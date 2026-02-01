# 🔐 SSH Access Guide - Clisonix Cloud

## Overview

Clisonix Cloud now includes a dedicated SSH server container that provides secure remote access to your Docker environment. This allows you to manage containers, access databases, view logs, and perform administrative tasks remotely.

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- SSH client installed on your local machine
- SSH key pair (or generate one)

### 1. Generate SSH Key Pair (If You Don't Have One)

```bash
# Generate a new ED25519 key (recommended)
ssh-keygen -t ed25519 -C "your-email@example.com" -f ~/.ssh/clisonix_cloud

# Or generate RSA key (if ED25519 not supported)
ssh-keygen -t rsa -b 4096 -C "your-email@example.com" -f ~/.ssh/clisonix_cloud
```

This will create two files:
- `~/.ssh/clisonix_cloud` - Your private key (KEEP THIS SECRET!)
- `~/.ssh/clisonix_cloud.pub` - Your public key (safe to share)

### 2. Add Your Public Key

Copy your public key and add it to the `authorized_keys` file:

```bash
# View your public key
cat ~/.ssh/clisonix_cloud.pub

# Add it to authorized_keys (on the server)
cat ~/.ssh/clisonix_cloud.pub >> infra/ssh/authorized_keys

# Or manually edit the file
nano infra/ssh/authorized_keys
```

The public key should look like:
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI... your-email@example.com
```

### 3. Setup SSH Server

Run the setup script to configure everything:

```bash
# Run from project root
./scripts/setup-ssh.sh
```

This script will:
- Create necessary directories
- Setup authorized_keys file
- Set correct permissions (600)
- Create log directories
- Verify Docker network

### 4. Start SSH Server

```bash
# Start SSH service
docker-compose -f docker-compose.ssh.yml up -d

# Verify it's running
docker-compose -f docker-compose.ssh.yml ps
docker logs clisonix-ssh
```

### 5. Connect to Your Server

```bash
# Connect via SSH (using custom port 2222)
ssh -i ~/.ssh/clisonix_cloud -p 2222 root@your-server-ip

# Example with specific IP
ssh -i ~/.ssh/clisonix_cloud -p 2222 root@157.90.234.158

# Or via localhost (for local development)
ssh -i ~/.ssh/clisonix_cloud -p 2222 root@localhost
```

On successful connection, you'll see:
```
════════════════════════════════════════════════════════════
  CLISONIX CLOUD - SSH ACCESS
════════════════════════════════════════════════════════════

Available Commands:
  docker ps              - List running containers
  docker logs <name>     - View container logs
  docker exec -it <name> - Enter container shell
  psql -h postgres ...   - Connect to PostgreSQL
  redis-cli -h redis     - Connect to Redis
```

## 🔧 Common Operations

### Managing Docker Containers

```bash
# List all running containers
docker ps

# View specific container logs
docker logs clisonix-api
docker logs -f clisonix-api  # Follow logs

# Execute commands in a container
docker exec -it clisonix-api bash

# Restart a container
docker restart clisonix-api

# View container stats
docker stats
```

### Database Access

#### PostgreSQL

```bash
# Connect to PostgreSQL
psql -h postgres -U clisonix -d clisonixdb

# Run a quick query
psql -h postgres -U clisonix -d clisonixdb -c "SELECT version();"

# Backup database
pg_dump -h postgres -U clisonix clisonixdb > backup.sql
```

#### Redis

```bash
# Connect to Redis CLI
redis-cli -h redis

# Check Redis info
redis-cli -h redis INFO

# Get specific keys
redis-cli -h redis KEYS "session:*"
```

### Viewing Logs

```bash
# View all container logs
docker-compose logs

# View specific service logs
docker-compose logs api
docker-compose logs postgres

# Follow logs in real-time
docker-compose logs -f api
```

### System Monitoring

```bash
# View resource usage
htop

# Check disk usage
df -h

# View network connections
netstat -tuln

# Check memory usage
free -h
```

## 🔒 Security Configuration

### SSH Security Features

The SSH server is configured with these security settings:

- ✅ **Key-based authentication only** - No passwords allowed
- ✅ **Non-standard port (2222)** - Reduces automated attacks
- ✅ **Root login with key only** - No password-based root login
- ✅ **Disabled features**: X11 forwarding, password authentication
- ✅ **Connection limits**: MaxSessions=10, MaxAuthTries=3
- ✅ **Automatic disconnection**: ClientAliveInterval/CountMax
- ✅ **Security banner**: Displays warning on connection

### Firewall Configuration

If using UFW (Uncomplicated Firewall):

```bash
# Allow SSH from anywhere (less secure)
ufw allow 2222/tcp

# Allow SSH from specific IP only (more secure)
ufw allow from 203.0.113.0/24 to any port 2222 proto tcp

# Check status
ufw status
```

### Best Practices

1. **Protect Your Private Key**
   ```bash
   # Ensure private key has correct permissions
   chmod 600 ~/.ssh/clisonix_cloud
   ```

2. **Use SSH Agent** (optional but convenient)
   ```bash
   # Start SSH agent
   eval "$(ssh-agent -s)"
   
   # Add your key
   ssh-add ~/.ssh/clisonix_cloud
   
   # Now you can connect without -i flag
   ssh -p 2222 root@your-server-ip
   ```

3. **Use SSH Config** (for easier connections)
   
   Add to `~/.ssh/config`:
   ```
   Host clisonix
       HostName your-server-ip
       Port 2222
       User root
       IdentityFile ~/.ssh/clisonix_cloud
       IdentitiesOnly yes
   ```
   
   Then connect simply with:
   ```bash
   ssh clisonix
   ```

4. **Regular Key Rotation**
   - Rotate SSH keys every 6-12 months
   - Remove old/unused keys from `authorized_keys`

5. **Monitor Access**
   ```bash
   # View SSH login attempts
   docker logs clisonix-ssh
   
   # View active SSH connections
   docker exec clisonix-ssh ps aux | grep sshd
   ```

6. **Docker Socket Security**
   
   ⚠️ **Important**: The SSH container has read-only access to the Docker socket, which allows viewing and executing commands in containers. While the socket is mounted as `:ro` (read-only), users can still:
   
   - ✅ View containers, logs, and stats
   - ✅ Execute commands in existing containers (`docker exec`)
   - ❌ Create, remove, or modify containers
   - ❌ Change Docker daemon configuration
   
   **Security implications**:
   - Users with SSH access can execute commands in containers that may have elevated privileges
   - Only grant SSH access to trusted administrators
   - Consider using `docker exec` with `--user` flag to limit privileges
   - Monitor Docker API calls if additional security is needed
   - For production, consider implementing additional access controls like Docker authorization plugins

## 🔧 Troubleshooting

### Connection Refused

**Problem**: `ssh: connect to host X port 2222: Connection refused`

**Solutions**:
```bash
# 1. Check if container is running
docker ps | grep clisonix-ssh

# 2. Check container logs
docker logs clisonix-ssh

# 3. Verify port is exposed
docker port clisonix-ssh

# 4. Check if port is open on host
netstat -tuln | grep 2222

# 5. Verify firewall rules
ufw status | grep 2222
```

### Permission Denied (publickey)

**Problem**: `Permission denied (publickey).`

**Solutions**:
```bash
# 1. Verify your public key is in authorized_keys
cat infra/ssh/authorized_keys

# 2. Check authorized_keys permissions (must be 600)
ls -la infra/ssh/authorized_keys
chmod 600 infra/ssh/authorized_keys

# 3. Verify you're using the correct private key
ssh -vvv -i ~/.ssh/clisonix_cloud -p 2222 root@server-ip

# 4. Check private key permissions (should be 600)
chmod 600 ~/.ssh/clisonix_cloud
```

### Container Health Check Failed

**Problem**: Container shows as unhealthy

**Solutions**:
```bash
# 1. Check health status
docker inspect clisonix-ssh | grep -A 10 Health

# 2. Check SSH daemon is running
docker exec clisonix-ssh ps aux | grep sshd

# 3. Restart the container
docker restart clisonix-ssh

# 4. Rebuild if needed
docker-compose -f docker-compose.ssh.yml up -d --build
```

### Can't Access Docker Commands

**Problem**: `docker: command not found` inside SSH container

**Solutions**:
```bash
# The Docker socket is mounted read-only
# You can view containers but not create/modify them
# This is intentional for security

# You can:
docker ps          # ✅ View containers
docker logs        # ✅ View logs
docker inspect     # ✅ Inspect containers

# You cannot:
docker run         # ❌ Create containers
docker rm          # ❌ Remove containers
docker stop        # ❌ Stop containers
```

## 📋 Maintenance

### Update SSH Server

```bash
# Pull latest changes
git pull

# Rebuild SSH container
docker-compose -f docker-compose.ssh.yml up -d --build

# Verify update
docker logs clisonix-ssh
```

### Backup SSH Configuration

```bash
# Backup authorized_keys
cp infra/ssh/authorized_keys infra/ssh/authorized_keys.backup

# Or create dated backup
cp infra/ssh/authorized_keys infra/ssh/authorized_keys.$(date +%Y%m%d)
```

### Add New User Key

```bash
# Append new public key to authorized_keys
echo "ssh-ed25519 AAAAC3... new-user@example.com" >> infra/ssh/authorized_keys

# Verify it was added
tail -1 infra/ssh/authorized_keys

# No need to restart, changes are immediate
```

### Remove User Key

```bash
# Edit authorized_keys and remove the line
nano infra/ssh/authorized_keys

# Or use sed to remove a specific key
sed -i '/specific-key-identifier/d' infra/ssh/authorized_keys
```

## 🌐 Production Deployment

### Hetzner Cloud Setup

```bash
# 1. SSH to your Hetzner server
ssh root@157.90.234.158

# 2. Clone repository
cd /opt && git clone https://github.com/Kameleonlife/Clisonix-cloud.git

# 3. Add your public key
cd Clisonix-cloud
cat >> infra/ssh/authorized_keys << 'EOF'
ssh-ed25519 YOUR_PUBLIC_KEY_HERE your-email@example.com
EOF

# 4. Setup and start
./scripts/setup-ssh.sh
docker-compose -f docker-compose.ssh.yml up -d

# 5. Configure firewall
ufw allow 2222/tcp
ufw status
```

### AWS / Azure / GCP Setup

Similar steps apply, but ensure:
- Security group allows port 2222 inbound
- Network ACLs are configured
- Consider using VPN or bastion host for additional security

## 📚 Additional Resources

- [Main README](../README.md)
- [Security Guide](../SECURITY.md)
- [Deployment Guide](../DEPLOYMENT_SECURITY_GUIDE.md)
- [SSH Configuration](infra/ssh/README.md)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [OpenSSH Documentation](https://www.openssh.com/manual.html)

## 📞 Support

For issues or questions:
1. Check this guide and troubleshooting section
2. Review container logs: `docker logs clisonix-ssh`
3. Contact the Clisonix Cloud team
4. Create an issue on GitHub

---

**🔐 Remember**: Keep your private keys secure and never commit them to version control!

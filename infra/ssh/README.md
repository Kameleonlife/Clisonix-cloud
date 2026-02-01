# 🔐 SSH Server Configuration

This directory contains the SSH server configuration for secure remote access to the Clisonix Cloud Docker environment.

## 🚀 Quick Start

### 1. Generate SSH Key Pair (Local Machine)

```bash
# Generate a new SSH key pair
ssh-keygen -t ed25519 -C "your-email@example.com" -f ~/.ssh/clisonix_cloud

# Copy your public key
cat ~/.ssh/clisonix_cloud.pub
```

### 2. Add Your Public Key

Copy your public key content and add it to the `authorized_keys` file:

```bash
# On the server
echo "your-public-key-here" >> /home/runner/work/Clisonix-cloud/Clisonix-cloud/infra/ssh/authorized_keys
```

Or create the file if it doesn't exist:

```bash
cat > /home/runner/work/Clisonix-cloud/Clisonix-cloud/infra/ssh/authorized_keys << 'EOF'
ssh-ed25519 AAAAC3... your-email@example.com
EOF
```

### 3. Start SSH Service

```bash
# Using docker-compose
docker-compose -f docker-compose.ssh.yml up -d

# Or add to your main docker-compose.yml
docker-compose up -d ssh
```

### 4. Connect via SSH

```bash
# Connect to the SSH container
ssh -i ~/.ssh/clisonix_cloud -p 2222 root@your-server-ip

# Or via localhost if running locally
ssh -i ~/.ssh/clisonix_cloud -p 2222 root@localhost
```

## 🔒 Security Features

- **Key-based authentication only** - No password authentication
- **Non-standard port (2222)** - Reduces automated attacks
- **Minimal permissions** - Root login only with key
- **Connection monitoring** - All connections logged
- **Security banner** - Displays warning on connection
- **Restricted forwarding** - Limited tunnel capabilities

## 📋 Available Commands

Once connected, you can:

```bash
# View running containers
docker ps

# View container logs
docker logs clisonix-api

# Execute commands in containers
docker exec -it clisonix-api bash

# Connect to PostgreSQL
psql -h postgres -U clisonix -d clisonixdb

# Connect to Redis
redis-cli -h redis

# View system resources
htop
```

## 🛡️ Security Best Practices

1. **Use Strong Keys**: Always use ED25519 or RSA 4096-bit keys
2. **Protect Private Keys**: Never share your private key
3. **Use SSH Agent**: Use `ssh-agent` for key management
4. **Limit Access**: Only add public keys for authorized users
5. **Monitor Connections**: Regularly check `/var/log/auth.log`
6. **Rotate Keys**: Periodically rotate SSH keys
7. **Use Firewall**: Restrict port 2222 to known IPs

## 🔧 Troubleshooting

### Connection Refused

```bash
# Check if container is running
docker ps | grep ssh

# Check container logs
docker logs clisonix-ssh

# Verify port is exposed
netstat -tuln | grep 2222
```

### Permission Denied

```bash
# Verify authorized_keys permissions (must be 600)
chmod 600 infra/ssh/authorized_keys

# Check if your public key is in authorized_keys
cat infra/ssh/authorized_keys
```

### Container Health Issues

```bash
# Check health status
docker inspect clisonix-ssh | grep Health

# Restart the container
docker restart clisonix-ssh
```

## 📚 Configuration Files

- `Dockerfile` - SSH server container image
- `sshd_config` - OpenSSH server configuration
- `banner` - Login warning banner
- `authorized_keys` - Authorized SSH public keys (you create this)

## 🌐 Production Deployment

For production environments:

1. **Use separate authorized_keys per environment**
2. **Restrict port 2222 via firewall** (e.g., UFW, iptables)
3. **Enable audit logging** for compliance
4. **Use bastion host** for additional security layer
5. **Implement fail2ban** for brute-force protection

### Example UFW Rules

```bash
# Allow SSH from specific IP only
ufw allow from 203.0.113.0/24 to any port 2222 proto tcp

# Or allow from anywhere (less secure)
ufw allow 2222/tcp
```

## 📞 Support

For issues or questions, contact the Clisonix Cloud team or refer to the main [SECURITY.md](../../SECURITY.md) documentation.

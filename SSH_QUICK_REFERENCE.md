# 🔐 SSH Quick Reference - Clisonix Cloud

## Setup

```bash
# 1. Generate SSH key
ssh-keygen -t ed25519 -C "your-email@example.com" -f ~/.ssh/clisonix_cloud

# 2. Add public key to server
cat ~/.ssh/clisonix_cloud.pub >> infra/ssh/authorized_keys

# 3. Run setup
./scripts/setup-ssh.sh

# 4. Start SSH server
docker-compose -f docker-compose.ssh.yml up -d
```

## Connect

```bash
# Basic connection
ssh -i ~/.ssh/clisonix_cloud -p 2222 root@your-server-ip

# Local development
ssh -i ~/.ssh/clisonix_cloud -p 2222 root@localhost

# Production (example)
ssh -i ~/.ssh/clisonix_cloud -p 2222 root@157.90.234.158
```

## SSH Config (Optional)

Add to `~/.ssh/config` for easier access:

```
Host clisonix
    HostName your-server-ip
    Port 2222
    User root
    IdentityFile ~/.ssh/clisonix_cloud
    IdentitiesOnly yes
```

Then connect with: `ssh clisonix`

## Common Commands

### Docker Operations
```bash
docker ps                              # List containers
docker logs clisonix-api              # View logs
docker logs -f clisonix-api           # Follow logs
docker exec -it clisonix-api bash     # Enter container
docker stats                          # Resource usage
docker restart clisonix-api           # Restart container
```

### Database Access
```bash
# PostgreSQL
psql -h postgres -U clisonix -d clisonixdb
psql -h postgres -U clisonix -d clisonixdb -c "SELECT version();"

# Redis
redis-cli -h redis
redis-cli -h redis INFO
redis-cli -h redis KEYS "*"
```

### System Monitoring
```bash
htop                    # Interactive process viewer
df -h                   # Disk usage
free -h                 # Memory usage
netstat -tuln           # Network connections
```

### Log Management
```bash
# View SSH access logs
docker logs clisonix-ssh

# View application logs
docker-compose logs api
docker-compose logs -f api     # Follow logs

# Check all services
docker-compose ps
```

## Troubleshooting

### Connection Issues
```bash
# Check if SSH container is running
docker ps | grep ssh

# View SSH logs
docker logs clisonix-ssh

# Restart SSH container
docker restart clisonix-ssh
```

### Permission Issues
```bash
# Fix authorized_keys permissions
chmod 600 infra/ssh/authorized_keys

# Fix private key permissions
chmod 600 ~/.ssh/clisonix_cloud

# Verify key is added
cat infra/ssh/authorized_keys
```

### Firewall Issues
```bash
# Check if port is open
netstat -tuln | grep 2222

# Allow port through UFW
ufw allow 2222/tcp
ufw status
```

## Security

- ✅ **Only key-based authentication** - No passwords
- ✅ **Non-standard port 2222** - Reduces attacks
- ✅ **Read-only Docker socket** - Limited container access
- ✅ **Connection logging** - All access monitored

## Files

- `infra/ssh/Dockerfile` - SSH server image
- `infra/ssh/sshd_config` - SSH daemon configuration
- `infra/ssh/authorized_keys` - Authorized public keys (add yours here)
- `infra/ssh/banner` - Login warning message
- `docker-compose.ssh.yml` - SSH service configuration
- `scripts/setup-ssh.sh` - Automated setup script

## Documentation

- 📖 **Full Guide**: [SSH_ACCESS_GUIDE.md](SSH_ACCESS_GUIDE.md)
- 🔐 **Security**: [SECURITY.md](SECURITY.md)
- 🚀 **Deployment**: [HETZNER_DEPLOYMENT_GUIDE.md](HETZNER_DEPLOYMENT_GUIDE.md)

## Support

Need help? Check:
1. Full SSH guide: `SSH_ACCESS_GUIDE.md`
2. Container logs: `docker logs clisonix-ssh`
3. Setup script: `./scripts/setup-ssh.sh`

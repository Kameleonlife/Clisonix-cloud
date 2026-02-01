#!/bin/bash
#
# Clisonix Cloud - SSH Server Setup Script
# Configures SSH server for secure remote access
#
# Usage: ./scripts/setup-ssh.sh

set -e

echo "════════════════════════════════════════════════════════════"
echo "  CLISONIX CLOUD - SSH SERVER SETUP"
echo "════════════════════════════════════════════════════════════"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
SSH_DIR="infra/ssh"
AUTHORIZED_KEYS="$SSH_DIR/authorized_keys"
AUTHORIZED_KEYS_EXAMPLE="$SSH_DIR/authorized_keys.example"

# Check if running from project root
if [ ! -f "docker-compose.ssh.yml" ]; then
    echo -e "${RED}❌ Error: Please run this script from the project root directory${NC}"
    exit 1
fi

echo "[1/5] Checking SSH configuration directory..."
if [ ! -d "$SSH_DIR" ]; then
    echo -e "${RED}❌ SSH configuration directory not found${NC}"
    exit 1
fi
echo -e "${GREEN}✅ SSH directory found${NC}"
echo ""

echo "[2/5] Checking authorized_keys file..."
if [ ! -f "$AUTHORIZED_KEYS" ]; then
    echo -e "${YELLOW}⚠️  authorized_keys file not found${NC}"
    echo "   Creating from example file..."
    
    if [ -f "$AUTHORIZED_KEYS_EXAMPLE" ]; then
        cp "$AUTHORIZED_KEYS_EXAMPLE" "$AUTHORIZED_KEYS"
        echo -e "${GREEN}✅ Created authorized_keys from example${NC}"
    else
        touch "$AUTHORIZED_KEYS"
        echo -e "${GREEN}✅ Created empty authorized_keys${NC}"
    fi
    echo ""
    echo -e "${YELLOW}⚠️  WARNING: No SSH keys configured!${NC}"
    echo "   You need to add your public key to: $AUTHORIZED_KEYS"
    echo ""
    echo "   Generate a new key with:"
    echo "   ssh-keygen -t ed25519 -C \"your-email@example.com\" -f ~/.ssh/clisonix_cloud"
    echo ""
    echo "   Then add your public key:"
    echo "   cat ~/.ssh/clisonix_cloud.pub >> $AUTHORIZED_KEYS"
    echo ""
else
    echo -e "${GREEN}✅ authorized_keys file exists${NC}"
    
    # Count non-empty, non-comment lines
    KEY_COUNT=$(grep -c "^ssh-" "$AUTHORIZED_KEYS" || echo "0")
    
    if [ "$KEY_COUNT" -eq "0" ]; then
        echo -e "${YELLOW}⚠️  No SSH keys found in authorized_keys${NC}"
        echo "   Add your public key to: $AUTHORIZED_KEYS"
    else
        echo -e "${GREEN}✅ Found $KEY_COUNT SSH key(s) in authorized_keys${NC}"
    fi
fi
echo ""

echo "[3/5] Setting correct permissions..."
chmod 600 "$AUTHORIZED_KEYS"
echo -e "${GREEN}✅ Set authorized_keys permissions to 600${NC}"
echo ""

echo "[4/5] Creating logs directory..."
mkdir -p logs/ssh
echo -e "${GREEN}✅ Logs directory created${NC}"
echo ""

echo "[5/5] Checking Docker network..."
if docker network ls | grep -q "clisonix-cloud_clisonix"; then
    echo -e "${GREEN}✅ Docker network exists${NC}"
else
    echo -e "${YELLOW}⚠️  Docker network not found, creating it...${NC}"
    docker network create clisonix-cloud_clisonix || echo -e "${YELLOW}Network may already exist${NC}"
fi
echo ""

echo "════════════════════════════════════════════════════════════"
echo -e "${GREEN}  SSH SERVER SETUP COMPLETE!${NC}"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Add your SSH public key to authorized_keys:"
echo "   cat ~/.ssh/your_key.pub >> $AUTHORIZED_KEYS"
echo ""
echo "2. Start the SSH server:"
echo "   docker-compose -f docker-compose.ssh.yml up -d"
echo ""
echo "3. Connect via SSH:"
echo "   ssh -i ~/.ssh/your_key -p 2222 root@your-server-ip"
echo ""
echo "4. Check server status:"
echo "   docker-compose -f docker-compose.ssh.yml ps"
echo "   docker logs clisonix-ssh"
echo ""
echo "════════════════════════════════════════════════════════════"
echo ""

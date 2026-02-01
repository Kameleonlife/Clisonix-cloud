#!/bin/bash
#
# Clisonix Cloud - SSH Server Demo
# Demonstrates SSH server setup and common operations
#

set -e

echo "════════════════════════════════════════════════════════════"
echo "  CLISONIX CLOUD - SSH SERVER DEMO"
echo "════════════════════════════════════════════════════════════"
echo ""

# Configuration
SERVER_IP="${SERVER_IP:-localhost}"
SSH_PORT="${SSH_PORT:-2222}"
SSH_KEY="${SSH_KEY:-$HOME/.ssh/clisonix_cloud}"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Step 1: Check if SSH key exists
echo -e "${BLUE}[1/7] Checking SSH Key...${NC}"
if [ ! -f "$SSH_KEY" ]; then
    echo -e "${YELLOW}⚠️  SSH key not found at: $SSH_KEY${NC}"
    echo "   Generating new SSH key pair..."
    ssh-keygen -t ed25519 -C "clisonix-demo@example.com" -f "$SSH_KEY" -N ""
    echo -e "${GREEN}✅ SSH key generated${NC}"
else
    echo -e "${GREEN}✅ SSH key found${NC}"
fi
echo ""

# Step 2: Display public key
echo -e "${BLUE}[2/7] Your SSH Public Key:${NC}"
echo "────────────────────────────────────────────────────────────"
cat "${SSH_KEY}.pub"
echo "────────────────────────────────────────────────────────────"
echo ""
echo -e "${YELLOW}📋 Add this public key to: infra/ssh/authorized_keys${NC}"
echo ""
read -p "Press Enter when you've added the key to authorized_keys..."
echo ""

# Step 3: Run setup script
echo -e "${BLUE}[3/7] Running SSH Setup Script...${NC}"
if [ -f "./scripts/setup-ssh.sh" ]; then
    ./scripts/setup-ssh.sh
    echo -e "${GREEN}✅ Setup complete${NC}"
else
    echo -e "${YELLOW}⚠️  Setup script not found, skipping...${NC}"
fi
echo ""

# Step 4: Start SSH server
echo -e "${BLUE}[4/7] Starting SSH Server...${NC}"
docker-compose -f docker-compose.ssh.yml up -d
echo ""
echo -e "${GREEN}✅ SSH server started${NC}"
echo ""

# Wait for SSH to be ready
echo "Waiting for SSH server to be ready..."
sleep 5

# Step 5: Test connection
echo -e "${BLUE}[5/7] Testing SSH Connection...${NC}"
echo "Connecting to: root@${SERVER_IP}:${SSH_PORT}"
echo ""

# Test SSH connection
# Using accept-new instead of 'no' for better security - accepts new keys once
# and validates them on subsequent connections
if ssh -i "$SSH_KEY" -p "$SSH_PORT" -o StrictHostKeyChecking=accept-new -o UserKnownHostsFile=/dev/null -o ConnectTimeout=5 root@"$SERVER_IP" "echo 'SSH connection successful!'" 2>/dev/null; then
    echo -e "${GREEN}✅ SSH connection test passed${NC}"
else
    echo -e "${YELLOW}⚠️  Could not connect via SSH${NC}"
    echo "   Check if:"
    echo "   1. Your public key is in infra/ssh/authorized_keys"
    echo "   2. The SSH container is running: docker ps | grep ssh"
    echo "   3. Port 2222 is accessible"
fi
echo ""

# Step 6: Demonstrate common operations
echo -e "${BLUE}[6/7] Demonstrating Common Operations:${NC}"
echo ""

echo "📦 Listing Docker Containers:"
ssh -i "$SSH_KEY" -p "$SSH_PORT" -o StrictHostKeyChecking=accept-new -o UserKnownHostsFile=/dev/null root@"$SERVER_IP" "docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'" 2>/dev/null || echo "  (Connection failed)"
echo ""

echo "💾 Checking System Resources:"
ssh -i "$SSH_KEY" -p "$SSH_PORT" -o StrictHostKeyChecking=accept-new -o UserKnownHostsFile=/dev/null root@"$SERVER_IP" "df -h | head -5" 2>/dev/null || echo "  (Connection failed)"
echo ""

# Step 7: Show next steps
echo -e "${BLUE}[7/7] Next Steps:${NC}"
echo ""
echo "🔐 Connect to SSH server:"
echo "   ssh -i $SSH_KEY -p $SSH_PORT root@$SERVER_IP"
echo ""
echo "📊 View logs:"
echo "   docker logs clisonix-ssh"
echo ""
echo "🛑 Stop SSH server:"
echo "   docker-compose -f docker-compose.ssh.yml down"
echo ""
echo "📖 Full documentation:"
echo "   - SSH_ACCESS_GUIDE.md"
echo "   - SSH_QUICK_REFERENCE.md"
echo ""
echo "════════════════════════════════════════════════════════════"
echo -e "${GREEN}  SSH SERVER DEMO COMPLETE!${NC}"
echo "════════════════════════════════════════════════════════════"
echo ""

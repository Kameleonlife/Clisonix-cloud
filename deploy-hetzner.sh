#!/bin/bash
#
# Clisonix Cloud - Hetzner Production Deployment Script
# Auto-installs Docker, configures services, and deploys the platform
#
# Usage: curl -fsSL https://raw.githubusercontent.com/LedjanAhmati/Clisonix-cloud/main/deploy-hetzner.sh | bash
#

set -e

echo "════════════════════════════════════════════════════════════"
echo "  CLISONIX CLOUD - HETZNER DEPLOYMENT"
echo "════════════════════════════════════════════════════════════"
echo ""

# Configuration
SERVER_IP="${SERVER_IP:-$(curl -s ifconfig.me)}"
DOMAIN="${DOMAIN:-clisonix.com}"
API_DOMAIN="${API_DOMAIN:-api.clisonix.com}"
PROJECT_DIR="/opt/clisonix"

echo "📍 Server IP: $SERVER_IP"
echo "🌐 Domain: $DOMAIN"
echo "🔌 API Domain: $API_DOMAIN"
echo ""

# Step 1: System Update
echo "[1/8] Updating system..."
apt update -y && apt upgrade -y
apt install -y ca-certificates curl gnupg lsb-release git ufw

# Step 2: Install Docker
echo ""
echo "[2/8] Installing Docker..."
if ! command -v docker &> /dev/null; then
    install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    chmod a+r /etc/apt/keyrings/docker.gpg
    
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    apt update -y
    apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    
    systemctl enable docker
    systemctl start docker
    
    echo "✅ Docker installed: $(docker --version)"
else
    echo "✅ Docker already installed: $(docker --version)"
fi

# Step 3: Firewall Configuration
echo ""
echo "[3/8] Configuring firewall..."
ufw allow 22/tcp   # SSH
ufw allow 80/tcp   # HTTP
ufw allow 443/tcp  # HTTPS
ufw allow 8000/tcp # API (internal)
ufw allow 3000/tcp # Web (internal)
ufw allow 9090/tcp # Prometheus (optional)
ufw allow 3001/tcp # Grafana (optional)
echo "y" | ufw enable
echo "✅ Firewall configured"

# Step 4: Create Project Directory
echo ""
echo "[4/8] Creating project directory..."
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR
echo "✅ Project directory: $PROJECT_DIR"

# Step 5: Clone Repository
echo ""
echo "[5/8] Cloning Clisonix Cloud repository..."
if [ ! -d ".git" ]; then
    git clone https://github.com/LedjanAhmati/Clisonix-cloud.git .
else
    git pull origin main
fi
echo "✅ Repository cloned"

# Step 6: Create Production Environment File
echo ""
echo "[6/8] Creating production environment..."
cat > .env.production <<EOF
# Clisonix Cloud - Production Environment
ENV=production
NODE_ENV=production

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=https://$DOMAIN,https://www.$DOMAIN

# Frontend Configuration
NEXT_PUBLIC_API_URL=https://$API_DOMAIN

# Database (configure with your PostgreSQL)
DATABASE_URL=postgresql://user:password@localhost:5432/clisonix

# Redis
REDIS_URL=redis://localhost:6379

# Stripe (configure with your keys)
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...

# Security
SECRET_KEY=$(openssl rand -hex 32)
API_KEY=$(openssl rand -hex 16)

# Monitoring
PROMETHEUS_PORT=9090
GRAFANA_PORT=3001
EOF
echo "✅ Environment file created"

# Step 7: Create Docker Compose Configuration
echo ""
echo "[7/8] Creating Docker Compose configuration..."
cat > docker-compose.production.yml <<EOF
version: "3.9"

services:
  # Backend API
  api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: clisonix_api
    restart: unless-stopped
    ports:
      - "8000:8000"
    env_file:
      - .env.production
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    networks:
      - clisonix_network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Frontend Web
  web:
    build:
      context: .
      dockerfile: apps/web/Dockerfile
    container_name: clisonix_web
    restart: unless-stopped
    ports:
      - "3000:3000"
    env_file:
      - .env.production
    networks:
      - clisonix_network
    depends_on:
      - api

  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    container_name: clisonix_nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
      - /etc/letsencrypt:/etc/letsencrypt:ro
    networks:
      - clisonix_network
    depends_on:
      - api
      - web

  # PostgreSQL Database
  postgres:
    image: postgres:16-alpine
    container_name: clisonix_postgres
    restart: unless-stopped
    environment:
      POSTGRES_DB: clisonix
      POSTGRES_USER: clisonix
      POSTGRES_PASSWORD: \${DATABASE_PASSWORD:-changeme}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - clisonix_network
    ports:
      - "5432:5432"

  # Redis Cache
  redis:
    image: redis:7-alpine
    container_name: clisonix_redis
    restart: unless-stopped
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    networks:
      - clisonix_network
    ports:
      - "6379:6379"

  # Prometheus (Monitoring)
  prometheus:
    image: prom/prometheus:latest
    container_name: clisonix_prometheus
    restart: unless-stopped
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus_data:/prometheus
    networks:
      - clisonix_network
    ports:
      - "9090:9090"

  # Grafana (Dashboards)
  grafana:
    image: grafana/grafana:latest
    container_name: clisonix_grafana
    restart: unless-stopped
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=\${GRAFANA_PASSWORD:-admin}
      - GF_SERVER_ROOT_URL=https://grafana.$DOMAIN
    volumes:
      - grafana_data:/var/lib/grafana
    networks:
      - clisonix_network
    ports:
      - "3001:3000"
    depends_on:
      - prometheus

networks:
  clisonix_network:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
  prometheus_data:
  grafana_data:
EOF
echo "✅ Docker Compose configuration created"

# Step 8: Create Nginx Configuration
echo ""
echo "[8/8] Creating Nginx configuration..."
cat > nginx.conf <<'EOF'
events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Logging
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/json application/javascript application/xml+rss;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=web_limit:10m rate=30r/s;

    # Frontend - clisonix.com
    server {
        listen 80;
        server_name clisonix.com www.clisonix.com;

        location /.well-known/acme-challenge/ {
            root /var/www/certbot;
        }

        location / {
            return 301 https://$host$request_uri;
        }
    }

    server {
        listen 443 ssl http2;
        server_name clisonix.com www.clisonix.com;

        ssl_certificate /etc/letsencrypt/live/clisonix.com/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/clisonix.com/privkey.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;

        client_max_body_size 50M;

        location / {
            limit_req zone=web_limit burst=20 nodelay;
            
            proxy_pass http://web:3000;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_cache_bypass $http_upgrade;
        }
    }

    # API - api.clisonix.com
    server {
        listen 80;
        server_name api.clisonix.com;

        location /.well-known/acme-challenge/ {
            root /var/www/certbot;
        }

        location / {
            return 301 https://$host$request_uri;
        }
    }

    server {
        listen 443 ssl http2;
        server_name api.clisonix.com;

        ssl_certificate /etc/letsencrypt/live/api.clisonix.com/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/api.clisonix.com/privkey.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;

        client_max_body_size 50M;

        location / {
            limit_req zone=api_limit burst=10 nodelay;
            
            proxy_pass http://api:8000;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
EOF
echo "✅ Nginx configuration created"

# Final Instructions
echo ""
echo "════════════════════════════════════════════════════════════"
echo "  ✅ INSTALLATION COMPLETE!"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "Next steps:"
echo ""
echo "1. Configure DNS at STRATO:"
echo "   - A Record: clisonix.com → $SERVER_IP"
echo "   - A Record: www.clisonix.com → $SERVER_IP"
echo "   - A Record: api.clisonix.com → $SERVER_IP"
echo ""
echo "2. Wait for DNS propagation (5-30 minutes)"
echo "   Check with: nslookup clisonix.com"
echo ""
echo "3. Install SSL certificates:"
echo "   apt install -y certbot"
echo "   certbot certonly --standalone -d clisonix.com -d www.clisonix.com"
echo "   certbot certonly --standalone -d api.clisonix.com"
echo ""
echo "4. Start the platform:"
echo "   cd $PROJECT_DIR"
echo "   docker compose -f docker-compose.production.yml up -d --build"
echo ""
echo "5. Monitor deployment:"
echo "   docker compose logs -f"
echo ""
echo "════════════════════════════════════════════════════════════"

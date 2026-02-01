# SSH Server for Clisonix Cloud
# Provides secure remote access to the Docker environment

FROM alpine:3.19

# Install OpenSSH server and necessary tools
RUN apk add --no-cache \
    openssh-server \
    openssh-client \
    bash \
    curl \
    docker-cli \
    postgresql-client \
    redis \
    nano \
    vim \
    htop \
    git \
    net-tools \
    && rm -rf /var/cache/apk/*

# Create SSH directory structure
RUN mkdir -p /var/run/sshd \
    && mkdir -p /root/.ssh \
    && chmod 700 /root/.ssh

# Configure SSH for secure access
RUN ssh-keygen -A && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin prohibit-password/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config && \
    sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/' /etc/ssh/sshd_config && \
    sed -i 's/#Port 22/Port 2222/' /etc/ssh/sshd_config

# Add welcome message
RUN echo '#!/bin/bash' > /etc/profile.d/welcome.sh && \
    echo 'cat << "EOF"' >> /etc/profile.d/welcome.sh && \
    echo '════════════════════════════════════════════════════════════' >> /etc/profile.d/welcome.sh && \
    echo '  CLISONIX CLOUD - SSH ACCESS' >> /etc/profile.d/welcome.sh && \
    echo '════════════════════════════════════════════════════════════' >> /etc/profile.d/welcome.sh && \
    echo '' >> /etc/profile.d/welcome.sh && \
    echo 'Available Commands:' >> /etc/profile.d/welcome.sh && \
    echo '  docker ps              - List running containers' >> /etc/profile.d/welcome.sh && \
    echo '  docker logs <name>     - View container logs' >> /etc/profile.d/welcome.sh && \
    echo '  docker exec -it <name> - Enter container shell' >> /etc/profile.d/welcome.sh && \
    echo '  psql -h postgres ...   - Connect to PostgreSQL' >> /etc/profile.d/welcome.sh && \
    echo '  redis-cli -h redis     - Connect to Redis' >> /etc/profile.d/welcome.sh && \
    echo '' >> /etc/profile.d/welcome.sh && \
    echo 'EOF' >> /etc/profile.d/welcome.sh && \
    chmod +x /etc/profile.d/welcome.sh

# Expose SSH port
EXPOSE 2222

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD netstat -tuln | grep -q ":2222" || exit 1

# Start SSH daemon
CMD ["/usr/sbin/sshd", "-D", "-e"]

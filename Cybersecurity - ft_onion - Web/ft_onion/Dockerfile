FROM debian:bullseye-slim

EXPOSE 80
EXPOSE 4242

LABEL description="Docker image for Tor hidden service with SSH and Nginx." \
      version="1.0"

# Install dependencies
RUN apt-get update && \
    apt-get install -y \
        curl \
        gnupg2 \
        apt-transport-https \
        openssh-server \
        nginx \
        libevent-dev \
        gpg && \
    apt-get clean

# Add Tor repository and install
RUN echo "deb https://deb.torproject.org/torproject.org bullseye main\ndeb-src https://deb.torproject.org/torproject.org bullseye main" >> /etc/apt/sources.list && \
    curl https://deb.torproject.org/torproject.org/A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89.asc | gpg --import && \
    gpg --export A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89 | apt-key add - && \
    apt-get update && \
    apt-get install -y tor deb.torproject.org-keyring && \
    apt-get autoremove -y && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Setup SSH and authorized_keys for root
RUN mkdir -p /run/sshd /root/.ssh
COPY ./secrets/id_rsa.pub /root/.ssh/authorized_keys
RUN chown -R root:root /root/.ssh && \
    chmod 700 /root/.ssh && \
    chmod 600 /root/.ssh/authorized_keys

# Copy SSH config (must allow root login)
COPY ./configs/sshd_config /etc/ssh/sshd_config

# Copy Nginx and Tor configs
COPY ./configs/nginx.conf /etc/nginx/nginx.conf
COPY ./configs/server_conf /etc/nginx/sites-available/default
COPY ./configs/torrc /etc/tor/torrc
RUN chown -R debian-tor /var/lib/tor

# Nginx logs to Docker stdout/stderr
RUN ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log

# Copy startup script
COPY ./start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]

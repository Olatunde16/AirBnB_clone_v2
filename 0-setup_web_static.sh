#!/usr/bin/env bash

# Install Nginx if not already installed
if ! [ -x "$(command -v nginx)" ]; then
    apt-get update
    apt-get install -y nginx
fi

# Create necessary folders if they don't exist
mkdir -p /data/web_static/releases/test /data/web_static/shared

# Create a fake HTML file for testing
echo "Holberton School" > /data/web_static/releases/test/index.html

# Create symbolic link and ensure it's updated
rm -rf /data/web_static/current
ln -sf /data/web_static/releases/test /data/web_static/current

# Set ownership recursively
chown -R ubuntu:ubuntu /data/
chgrp -R ubuntu /data/

# Update Nginx configuration
config_block="
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By $HOSTNAME;
    root   /var/www/html;
    index  index.html index.htm;

    location /hbnb_static/ {
        alias /data/web_static/current/;
        index index.html index.htm;
    }

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }

    location /redirect_me {
        return 301 http://youtube.com/;
    }

    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}
"
echo "$config_block" > /etc/nginx/sites-available/default

# Restart Nginx to apply changes
service nginx restart

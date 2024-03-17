#!/usr/bin/env bash
# Sets up webservers for deployment: (Run script on both servers)

WEBSTATIC="\\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n"

sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get -y install nginx
#run as root and make the two main dir
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared
#create index.html and echo text for testing
echo "This tests index.html on Nginx config" | sudo tee /data/web_static/releases/test/index.html
#create symbolic link(shortcut file)
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
#Give ownership of the /data/ folder to the ubuntu user
sudo chown -hR ubuntu:ubuntu /data/
sudo sed -i "35i $WEBSTATIC" /etc/nginx/sites-available/default
sudo service nginx start

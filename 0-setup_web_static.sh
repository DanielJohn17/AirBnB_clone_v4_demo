#!/usr/bin/env bash
#Sets up a web server for deployment of web_static.


apt-get -y update
apt-get -y upgrade

apt-get -y install nginx

mkdir -p /data/web_static/releases/test
mkdir -p /data/web_static/shared
echo "Daniel is cool!!!!" > /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test/ /data/web_static/current

chown -R ubuntu /data/
chgrp -R ubuntu /data/

sed -i "7i\\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n" /etc/nginx/sites-available/default

service nginx start

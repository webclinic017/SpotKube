#!/bin/bash

management_node="$1"

# Change directory to /etc/nginx
cd /etc/nginx/sites-available

# Create or edit the 'mgt_server' file
cat <<EOF | sudo tee spotkube
# Management server API
server {
    listen 80;
    server_name ${MGT_SERVER};
    location / {
        proxy_pass http://localhost:8000;
    }
}
EOF

# Create symlink
sudo ln -s /etc/nginx/sites-available/spotkube /etc/nginx/sites-enabled/

# Restart the nginx service
sudo systemctl restart nginx.service

# Build binary for elastic scalar
./../../../elastic_scalar/scripts/setup.sh

# Copy spotkube_ms.service to /etc/systemd/system
sudo cp spotkube_ms.service /etc/systemd/system/
sudo chown root:root /etc/systemd/system/spotkube_ms.service

# Copy spotkube_es.service to /etc/systemd/system
sudo cp spotkube_es.service /etc/systemd/system/
sudo chown root:root /etc/systemd/system/spotkube_es.service

# Reload systemd
sudo systemctl daemon-reload

# Start the spotkube service
sudo systemctl start spotkube_ms.service
# sudo systemctl start spotkube_es.service

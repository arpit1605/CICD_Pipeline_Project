#!/bin/bash

REPO_URL="https://github.com/arpit1605/CICD_Pipeline_Project.git"
CLONE_DIR="/mnt/d/Devops/CICD_Pipeline_Project/CICD_Pipeline"

# Clone the latest code
git clone "$REPO_URL" "$CLONE_DIR"

# Deploy the files
sudo cp -r "$CLONE_DIR/index.html" /var/www/html/

# Checking whether the copy was completed or not:
if [ $? -ne 0 ]; then
    echo "Error while copying the file"
    exit 1
fi

# Restart Nginx
sudo systemctl restart nginx

echo "Latest changes are deployment successfully and Nginx has beeen restarted."

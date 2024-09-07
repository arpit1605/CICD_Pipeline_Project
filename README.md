Building CI-CD Pipeline Tool: 

Create a complete CI-CD pipeline using bash, python, and crontabs. The list of tasks is specified below: 
Task 1: Set Up a Simple HTML Project. 
Create a simple HTML project and push it to a GitHub repository. 
Task 2: Set Up an AWS EC2/Local Linux Instance with Nginx
Task 3: Write a Python Script to Check for New Commits. 
Create a Python script to check for new commits using the GitHub API.
Task 4: Write a Bash Script to Deploy the Code. 
Create a bash script to clone the latest code and restart Nginx.
Task 5: Set Up a Cron Job to Run the Python Script. 
Create a cron job to run the Python script at regular intervals.
Task 6: Test the Setup. 
Make a new commit to the GitHub repository and check that the changes are automatically deployed. 

Steps to be followed:

Clone the repository to your local machine:
    git clone https://github.com/arpit1605/CICD_Pipeline_Project.git

Change the current working directory to the Project Directory
    cd CICD_Pipeline_Project

Create a new Branch
    git checkout main

Create an index.html file as below:
sudo touch index.html

Add the content to the index.html file:
sudo nano index.html

HTML
<!DOCTYPE html>
<html>
<head>
    <title>Simple HTML Project</title>
</head>
<body>
    <h1>Hello, World!</h1>
</body>
</html>

Push the changes to GitHub:
    git add .
    git commit -m "Added index.html file"
    git push -u origin main

Launch a local WSL Ubuntu Instance and install Nginx: 
Update the package list: 
    sudo apt-get update
Install Nginx:
    sudo apt-get install nginx -y
Enable nginx:
    sudo systemctl enable nginx
Check the status of nginx
    sudo systemctl status nginx
Start nginx:
    sudo systemctl start nginx

Install the required libraries to your local machine:
pip install requests
pip install subprocess

Create a project directory:
    mkdir CICD_Pipeline_Project
Change the current working directory to the Project Directory
    cd CICD_Pipeline_Project
Create checkCommits python file to check for new commits: 
    sudo touch checkCommits.py
Create deploy bash script file to deploy the changes:
    sudo touch deploy.sh

Add the below content to checkCommits.py file:

# Python Script to Check for New Commits:
import requests
import subprocess

def get_latest_commit_id(repo_owner, repo_name):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits"
    response = requests.get(url)
    if response.status_code == 200:    
        commits = response.json()
        latest_sha = commits[0]['sha']  # Accessing the SHA of the first commit
        return latest_sha
    else:
        print(f"Failed to fetch commit id: {response.status_code}")
        return None

def read_saved_commit_id(file_path):
    try:
        with open(file_path, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

def write_commit_id_to_file(file_path, commit_id):
    try:
        with open(file_path, "w") as file:
            file.write(commit_id)
    except IOError:
        print(f"Error writing to {file_path}")

if __name__ == "__main__":
    owner = "arpit1605"
    repo = "CICD_Pipeline_Project"
    saved_commit_file = "/mnt/d/Devops/CICD_Pipeline_Project/latest_commit.txt"

    latest_commit_id = get_latest_commit_id(owner, repo)
    saved_commit_id = read_saved_commit_id(saved_commit_file)

    if latest_commit_id and saved_commit_id:
        if latest_commit_id != saved_commit_id:
            print("New commit detected. Deploying changes...")
            # Run your deployment script here
            subprocess.run(["/mnt/d/Devops/CICD_Pipeline_Project/deploy.sh"])
            # Update the saved commit ID
            write_commit_id_to_file(saved_commit_file, latest_commit_id)
        else:
            print("No new commits made since the last deployment.")
    else:
        print("Error retrieving commit IDs.")


Add the below content to deploy.sh file

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

echo "Latest changes are deployed successfully and Nginx has been restarted."


Make the Script Executable:
chmod +x /mnt/d/Devops/CICD_Pipeline_Project/deploy.sh

Set Up a Cron Job to Run the Python Script
Edit the Crontab:
    crontab -e

Add the following line to run the Python script every 15 minutes:
    */15 * * * * /usr/bin/python3 /mnt/d/Devops/CICD_Pipeline_Project/checkCommits.py

Verify that the new cron job is set up correctly
    crontab -l


Testing the Setup:
Make changes to your HTML project and push it to GitHub:
echo "<p>New content</p>" >> index.html
git add .
git commit -m "Added new content"
git push origin main

Check Deployment:
Verify that the changes are automatically deployed to your server.

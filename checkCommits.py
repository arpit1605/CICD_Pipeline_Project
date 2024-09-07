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
    repo = "sample"
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

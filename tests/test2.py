import requests
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv(override=True)

def get_github_org_repos(user, token):
    """Fetches specific repository details (name, html_url, and created_at) for a GitHub organization."""
    url = f"https://api.github.com/users/{user}/repos?sort=updated"  

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        repos = response.json()
        if repos:
            repo_list = []
            for repo in repos:
                # Extract only the necessary fields
                repo_data = repo
                # repo_data = {
                #     "name": repo.get("name"),
                #     "html_url": repo.get("html_url"),
                #     "created_at": repo.get("created_at")
                # }
                repo_list.append(repo_data)

            # Save the extracted data into a file (or any storage method)
            with open("repositories.json", "w") as file:
                json.dump(repo_list, file, indent=4)
            print(f"Repositories data saved to repositories.json.")
        else:
            print(f"No repositories found for organization: {org}")
    else:
        print(f"Failed to fetch repositories: {response.status_code}, {response.text}")

# Get GitHub token from environment variable
github_token = os.getenv("GITHUB_TOKEN")

# Ensure the token is available
if not github_token:
    print("Error: GITHUB_TOKEN not found in environment variables.")
else:
    # Fetch and save repositories data for the specified organization
    get_github_org_repos("ELhadratiOth", github_token)  

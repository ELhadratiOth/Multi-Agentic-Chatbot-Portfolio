#getting details of a special repo

import base64
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(override=True)

def get_github_file(owner, repo, path, token):
    """Fetches and decodes a file (e.g., README.md) from a GitHub repository."""
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        file_data = response.json()
        file_content = base64.b64decode(file_data['content']).decode('utf-8')
        return file_content
    else:
        print(f"Failed to fetch file: {response.status_code}, {response.text}")
        return None

# Get GitHub token from environment variable
github_token = os.getenv("GITHUB_TOKEN")

# Ensure the token is available
if not github_token:
    print("Error: GITHUB_TOKEN not found in environment variables.")
else:
    # Fetch README.md from the repository
    readme_text = get_github_file("ELhadratiOth", "ENSAH-ChatBot-RAG-APP", "README.md", github_token)

    if readme_text:
        print("README CONTENT:\n")
        print(readme_text)

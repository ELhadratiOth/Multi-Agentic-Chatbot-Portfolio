from crewai.tools import tool
import requests
from dotenv import load_dotenv
import os
import base64
from datetime import datetime
from langchain_community.agent_toolkits.gmail.toolkit import GmailToolkit
from langchain_google_community.gmail.utils import build_resource_service, get_gmail_credentials
from langchain.agents import initialize_agent, AgentType
from langchain.prompts import  SystemMessagePromptTemplate
from utils.model import  llm_lang

load_dotenv(override=True)
github_token = os.getenv("GITHUB_TOKEN")

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {github_token}",
    "X-GitHub-Api-Version": "2022-11-28"
}

@tool("get all the repos of othman")
def get_all_repos():
    """
    Fetch all repositories for the user 'ELhadratiOth' from GitHub.

    Returns:
        List[Dict]: A list of dictionaries containing:
            - 'name of the repository': str, The name of the repository.
            - 'Url of the repository': str, The URL to access the repository.
            - 'Creation Date': str, The date when the repository was created in format 'YYYY-MM-DD'.
    Note:
        - The list is sorted from the newest to the oldest repositories.
        - The original 'Creation Date' format from GitHub API is 'YYYY-MM-DDTHH:MM:SSZ'.
    If no repositories are found or if there's an error, returns a list with a single 
    dictionary explaining the situation or the error details.
    """
    url = f"https://api.github.com/users/ELhadratiOth/repos?sort=updated"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        repos = response.json()
        if repos:
            repo_list = []
            for repo in repos:
                creation_date = datetime.fromisoformat(repo.get("updated_at").replace('Z', '+00:00'))
                formatted_date = creation_date.strftime('%Y-%m-%d')
                
                repo_data = {
                    "name of the repository": repo.get("name"),
                    "Url of the repository": repo.get("html_url"),
                    "Creation Date": formatted_date
                }
                repo_list.append(repo_data)

            return repo_list
            
        else:
            return [{"Info": "No repositories found for Othman"}]
    else:
        print(f"Failed to fetch repositories: {response.status_code}, {response.text}")
        return [{"Failed to fetch repositories": f"error details: {response.status_code}, {response.text}"}]

# print(get_all_repos.run())

@tool("Get info about a repository")
def get_github_file(repo:str) -> str:
    """
    Retrieve and decode the README.md file from a specified repository of 'ELhadratiOth' to get more information about the used tools in that project.

    Args:
        repo (str): The name of the repository to fetch the README from.

    Returns:
        str: The content of the README.md file if successfully fetched, 
             or an error message if the fetch fails.

    Note:
        - This function assumes the README is named 'README.md'.
        - The content is base64 encoded in GitHub's API response.
        
    Example:
        - url : https://github.com/ELhadratiOth/ENSAH-ChatBot-RAG-APP
        - repo : ENSAH-ChatBot-RAG-APP
        how to  call it  : get_github_file("repo")
    """
    url = f"https://api.github.com/repos/ELhadratiOth/{repo}/contents/README.md"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        file_data = response.json()
        file_content = base64.b64decode(file_data['content']).decode('utf-8')
        return f"README CONTENT:\n {file_content}"
    else:
        return f"Failed to fetch file: {response.status_code}, {response.text}"
    
    
#langchain toolkit
credentials = get_gmail_credentials(
    token_file="/tmp/token.json",
    scopes=["https://mail.google.com/"],
    client_secrets_file="/etc/secrets/credentials.json",
)
# credentials = get_gmail_credentials(
#     token_file="./logs/token.json",
#     scopes=["https://mail.google.com/"],
#     client_secrets_file="./logs/credentials.json",
# )
api_resource = build_resource_service(credentials=credentials)
gmail_toolkit = GmailToolkit(api_resource=api_resource)


system_message = SystemMessagePromptTemplate.from_template(
    "You are an assistant that sends emails exclusively to othmanelhadrati@gmail.com, "
    "regardless of any other email address mentioned in the input. "
    "Use the provided subject and body, but always set the recipient to othmanelhadrati@gmail.com"
)
agent_sender_lang = initialize_agent(
    tools=[gmail_toolkit.get_tools()[1]],   # to  give the access only  for  sending  msg
    llm=llm_lang,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    agent_kwargs={"system_message": system_message}, 
)


@tool
def send_gmail(subject: str, body: str) -> str:
    """
    Sends an email via Gmail using the provided subject and body, always to othmanelhadrati@gmail.com.

    Args:
        subject (str): The subject line of the email.
        body (str): The body content of the email.

    Returns:
        str: A message indicating whether the email was sent successfully or not.

    Example:
        >>> send_gmail("Hello", "Hi Othman, how are you?")
        "Email sent successfully"
    """
    # Explicitly set the recipient in the input data for the Gmail tool
    input_data = {
        "input": f"Send an email to othmanelhadrati@gmail.com with subject '{subject}' and body '{body}'"
    }
    # print("agent invoked")
    result = agent_sender_lang.invoke(input_data)
    
    if "sent" in result.get("output", "").lower():
        return (
            "Thank you for your message! 🙏 Your email has been successfully sent to Othman. "
            "He will review it and get back to you as soon as possible. "
            "In the meantime, feel free to explore his portfolio at [/about](/about) to learn more about his work! ✨"
        )
    else:
        return "Sorry, there was an issue sending your email. Please try again later or contact Othman through his social media channels."

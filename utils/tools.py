from crewai.tools import tool
import requests
from dotenv import load_dotenv
import os
import base64
from datetime import datetime
# from langchain_community.agent_toolkits.gmail.toolkit import GmailToolkit
# from langchain_google_community.gmail.utils import build_resource_service, get_gmail_credentials
# import json
# from google.oauth2.service_account import Credentials
# from langchain.agents import initialize_agent, AgentType
# from langchain.prompts import  SystemMessagePromptTemplate
# from utils.model import  llm_lang
import smtplib
from email.mime.text import MIMEText
import google.generativeai as genai

load_dotenv(override=True)
github_token = os.getenv("GITHUB_TOKEN")
app_password = os.getenv("GMAIL_APP_PASSWORD")

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
    url = f"https://api.github.com/users/ELhadratiOth/repos?sort=created"
    
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




@tool
def send_gmail(subject: str, body: str) -> str:
    """
    Send an email using Gmail SMTP.
    
    Args:
        subject (str): The subject of the email
        body (str): The body content of the email
        
    Returns:
        str: A message indicating the success or failure of sending the email
    """
    try:
        sender_email = "othmanelhadrati@gmail.com"
        receiver_email = "othmanelhadrati@gmail.com"  
        # print("suuuuuuuuuuuuuuuub : " +subject)
        message = MIMEText(body)
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject

        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            
        return (
            "email sent"
        )
        
    except ValueError :
        return "email not sent 1"
        
    except smtplib.SMTPAuthenticationError:
        return "email not sent 2"
        
    except Exception :
        return "email not sent 3"
    

@tool("Audio Transcription Tool")
def transcribe_audio(file_path: str) -> str:
    """
    Transcribe an audio file.

    Args:
        file_path (str): The path to the audio file to transcribe. 
                        Use forward slashes (/) or double backslashes (\\\\) in paths.
                        Examples: 
                        - "audios/audio.wav" (Linux/Unix style)
                        - "audios\\\\audio.wav" (Windows style with escaped backslashes)
                        - "/tmp/audio.wav" (Absolute path)
        
    Returns:
        str: The transcribed text from the audio file, or an error message if transcription fails
        
    Note:
        - Supports common audio formats (wav)
    """
    try:
        # Configure the Gemini API
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        
        # Normalize the file path to handle both Windows and Linux
        normalized_path = os.path.normpath(file_path)
        
        # Check if file exists
        if not os.path.exists(normalized_path):
            return f"Error: File not found at path: {normalized_path}"
        
        # Upload the audio file
        audio_file = genai.upload_file(normalized_path)
        
        # Create the model
        model = genai.GenerativeModel("gemini-2.5-pro")
        
        # Transcribe the audio
        prompt = "Transcribe this audio file. Only return the transcribed text, nothing else."
        response = model.generate_content([prompt, audio_file])
        
        # Clean up the uploaded file from Gemini's storage
        genai.delete_file(audio_file.name)
        
        return response.text.strip()
        
    except FileNotFoundError:
        return f"Error: Audio file not found at {normalized_path if 'normalized_path' in locals() else file_path}"
    except Exception as e:
        return f"Error during transcription: {str(e)}"

# send_gmail("salam","salam") 

# print(transcribe_audio("C:\\Users\\othma\\Downloads\\wav.wav"))
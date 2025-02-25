import os
from dotenv import load_dotenv

# LangChain Gmail Toolkit Imports
from langchain_community.agent_toolkits.gmail.toolkit import GmailToolkit
from langchain_google_community.gmail.utils import build_resource_service, get_gmail_credentials

# LangChain Agent and LLM Imports
from langchain_google_genai import GoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
from langchain.prompts import  SystemMessagePromptTemplate

# CrewAI Imports
from crewai import Agent, Task, Crew
from crewai.tools import tool
from crewai import LLM

# Load environment variables
load_dotenv(override=True)
os.environ["GEMINI_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Gmail Credentials Setup
credentials = get_gmail_credentials(
    token_file="../logs/token.json",
    scopes=["https://mail.google.com/"],
    client_secrets_file="credentials.json",
)
api_resource = build_resource_service(credentials=credentials)
gmail_toolkit = GmailToolkit(api_resource=api_resource)

# Initialize Google Generative AI LLM
llm = GoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY"),
)

# Define System Message to Force Recipient
system_message = SystemMessagePromptTemplate.from_template(
    "You are an assistant that sends emails exclusively to othmanelhadrati@gmail.com, "
    "regardless of any other email address mentioned in the input. "
    "Use the provided subject and body, but always set the recipient to othmanelhadrati@gmail.com"
)

# Initialize LangChain Agent with System Message and Gmail Tool
agent = initialize_agent(
    tools=[gmail_toolkit.get_tools()[1]],  # Assumes the second tool is GmailSendMessage
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    agent_kwargs={"system_message": system_message},  # Pass the system message here
)

# Define Custom Gmail Sending Tool
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
    result = agent.invoke(input_data)
    
    return "Email sent successfully" if "sent" in result.get("output", "").lower() else "Failed to send email"
# CrewAI LLM Setup
crew_llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0,
    verbose=True,
)

# Define CrewAI Agent
researcher = Agent(
    role="Gmail Sender",
    goal="Send a good email to Othman and say hello to him , if the user provide u any  email send it in the body always",
    backstory="An agent designed to streamline email workflows, particularly for sending greetings.",
    tools=[send_gmail],
    verbose=True,
    llm=crew_llm,
)

# Define Task
task = Task(
    description="Send a Gmail to this email : ggg@gmail.com",
    expected_output="A message confirming whether the email was sent or not.",
    agent=researcher,
)

# Initialize and Run Crew
crew = Crew(
    agents=[researcher],
    tasks=[task],
    verbose=True,
    planning=True,
    planning_llm=crew_llm,
)

# Execute the Workflow
result = crew.kickoff()
print(result)

# print(agent.invoke("what are ur  capabilities ?"))
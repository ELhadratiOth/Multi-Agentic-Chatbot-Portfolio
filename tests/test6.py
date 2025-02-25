from crewai import Agent, Task, Crew


from langchain_community.agent_toolkits.gmail.toolkit import GmailToolkit 
from langchain_community.tools.gmail.send_message import GmailSendMessage

from langchain_google_community.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)
credentials = get_gmail_credentials(
    token_file="../logs/token.json",
    scopes=["https://mail.google.com/"],
    client_secrets_file="credentials.json",
)
api_resource = build_resource_service(credentials=credentials)
toolkit = GmailToolkit(api_resource=api_resource)

from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
import os
load_dotenv(override=True)
from langchain.agents import initialize_agent, AgentType

llm2  =  GoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY"),
)
# search = toolkit.get_tools()[1]


agent = initialize_agent(
    tools=[toolkit.get_tools()[1]],
    llm=llm2,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
)


def langchain_agent_executor(input_text: str) -> str:
    print("i am runinggggggggggggggggggg")
    try:
        response = agent.run(input_text)
        return response
    except Exception as e:
        return f"Error executing LangChain agent: {str(e)}"

from crewai import LLM

os.environ["GEMINI_API_KEY"] = os.getenv("GOOGLE_API_KEY")

llm=LLM(
        model="gemini/gemini-2.0-flash",
        temperature=0,
        verbose=True,    
        )
# Create a CrewAI agent and assign the executor function
crewai_agent = Agent(
    role='gmail sender agent',
    goal='Provide detailed analyses on various topics.',
    backstory="""An AI agent proficient in conducting in-depth research and analysis
    across multiple domains, utilizing advanced language models and tools.""",
    executor=langchain_agent_executor,
    verbose=True,
    llm=llm
)





import os
from dotenv import load_dotenv
from crewai import Agent
from crewai.tools import BaseTool
from pydantic import Field





task = Task(
    description='sending gmail to  othman : gmail : `othmandone@gmail.com` ',
    expected_output='informational msg to declare if  the  mail is  sent or not',
    agent=crewai_agent,
)
crew = Crew(
    agents=[crewai_agent],
    tasks=[task],
    verbose=True,
    planning=True,
    planning_llm=llm
    
)

crew.kickoff()


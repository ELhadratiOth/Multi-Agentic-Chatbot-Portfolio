
from langchain_community.agent_toolkits.gmail.toolkit import GmailToolkit 
from langchain_community.tools.gmail.send_message import GmailSendMessage

from langchain_google_community.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)
credentials = get_gmail_credentials(
    token_file="/etc/secrets/token.json",
    scopes=["https://mail.google.com/"],
    client_secrets_file="/etc/secrets/credentials.json",
)
api_resource = build_resource_service(credentials=credentials)
toolkit = GmailToolkit(api_resource=api_resource)

from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
import os
load_dotenv(override=True)
from langchain.agents import initialize_agent, AgentType

llm  =  GoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY"),
)
search = toolkit.get_tools()[1]


agent = initialize_agent(
    tools=[toolkit.get_tools()[1]],
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
)
# from crewai.agent import  


# print(agent.invoke("what are ur  capabilities ?"))

import os
from dotenv import load_dotenv
from crewai import Agent
from crewai.tools import BaseTool
from pydantic import Field


from crewai import LLM

os.environ["GEMINI_API_KEY"] = os.getenv("GOOGLE_API_KEY")

llm=LLM(
        model="gemini/gemini-2.0-flash",
        temperature=0,
        verbose=True,    
        )
class GmailTool(BaseTool):
    name: str = "Gmail tool"
    description: str = "tool for sending email to othman to his  account : othmanelhadrati@gmail.com"
    search: GmailSendMessage = Field(default_factory=GmailSendMessage)

    def _run(self) -> str:
        """Execute the search query and return results"""
        try:
            return self.search.run(query)
        except Exception as e:
            return f"Error performing search: {str(e)}"
# gg = GmailTool()

# print(gg._run(query="send hello to othman " ,tool_input=""))

from crewai import Agent
from crewai import Task  ,Crew

researcher = Agent(
    role='Gmail Sender',
    goal='send good email to  othman and say hello to him',
    backstory="""workflow to send to othman email""",
    tools=[gmailTool],
    verbose=True,
    llm=llm
)
task = Task(
    description='sending gmail to  othman , the  input  of the  tool : Tool Arguments: dict(\'query\': \'message\')',
    expected_output='informational msg to declare if  the  mail is  sent or not',
    agent=researcher,
)
crew = Crew(
    agents=[researcher],
    tasks=[task],
    verbose=True,
    planning=True,
    planning_llm=llm
    
)

crew.kickoff()


#local 
from crewai import  Crew , Process 
from utils.agents import all_repos_agent , about_repo_agent , agent_manager , general_agent
from utils.tasks import  task_manager
from utils.memory import get_last_6_memories
import  os 
from dotenv import load_dotenv

# from crewai.memory.long_term.long_term_memory import LongTermMemory  #for persistent chat storage
# from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage
# from crewai.memory.short_term.short_term_memory import ShortTermMemory
# from crewai.memory.storage.rag_storage import RAGStorage
# from crewai.memory.entity.entity_memory import EntityMemory

from mem0 import MemoryClient

load_dotenv(override=True)


os.environ["GEMINI_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ["MEM0_API_KEY"] = os.getenv("MEM0_API_KEY")
os.environ['GRPC_ENABLE_FORK_SUPPORT'] = '0'
os.environ['GRPC_POLL_STRATEGY'] = 'epoll1'


client = MemoryClient()


crew = Crew(
    agents=[ general_agent ,all_repos_agent , about_repo_agent],
    tasks=[task_manager],
    process=Process.hierarchical,
    verbose=True,
    manager_agent=agent_manager,
    output_log_file = "./logs/logs.json",
    
    # memory=True,
    # memory_config={
    #     "provider": "mem0",
    #     "config": {"user_id": "portfolio_agent" },
    # },
    # embedder={
    #     "provider": "google",
    #     "config": {
    #         "model": "models/text-embedding-004",
    #         "api_key": os.getenv("GOOGLE_API_KEY"),
    #     }
    # },
    # long_term_memory = LongTermMemory(
    #     storage=LTMSQLiteStorage(
    #         db_path="./memory/long_term_memory_storage.db"
    #     )
    # ),
    # short_term_memory = ShortTermMemory(
    #     storage = RAGStorage(
    #             embedder_config={
    #                 "provider": "google",
    #                 "config": {
    #                     "model": 'models/text-embedding-004',
    #                     "api_key": os.getenv("GOOGLE_API_KEY"),                      
    #                 }
    #             },
    #             type="short_term",
    #             path="./memory/"
    #         )
    #     ),
)






question = "What is your email address for professional contact?"

all_memories = client.get_all(user_id= "alex",output_format="v1.1")

memory= get_last_6_memories(all_memories)


response = crew.kickoff(inputs={"question": question ,"chat history": memory })

# print(memory)

messages = [
    {"role": "user", "content": question},
    {"role": "assistant", "content":response["response"] }
]

client.add(messages, user_id="alex", output_format="v1.1")


# print(response)

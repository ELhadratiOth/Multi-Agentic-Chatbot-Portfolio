from mem0 import MemoryClient
import  os 
from dotenv import load_dotenv
load_dotenv(override=True)
from utils.memory import get_last_6_memories

os.environ["GEMINI_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ["MEM0_API_KEY"] = os.getenv("MEM0_API_KEY")
os.environ['GRPC_ENABLE_FORK_SUPPORT'] = '0'
os.environ['GRPC_POLL_STRATEGY'] = 'epoll1'
client = MemoryClient()


messages = [
    {"role": "user", "content": "Hi, I'm 7mar"},
    {"role": "assistant", "content": "welcome  mr 7mar"}
]

# # The default output_format is v1.0
client.add(messages, user_id="", output_format="v1.1")

# To use the latest output_format, set the output_format parameter to "v1.1"

# query = "What is his  name ? "

# The default output_format is v1.0
# print(client.search(query, user_id="7mar", output_format="v1.1"))
print(client.get_all(user_id="" , output_format="v1.1" ))

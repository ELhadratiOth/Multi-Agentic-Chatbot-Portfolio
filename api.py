from fastapi import FastAPI, HTTPException, Request, Response  
from fastapi.middleware.cors import CORSMiddleware
from utils.base_models import ChatRequest, ChatResponse
from crewai import Crew, Process
from utils.agents import all_repos_agent, about_repo_agent, agent_manager, general_agent ,agent_sender
from utils.tasks import task_manager 
from utils.memory import get_first_10_memories
from mem0 import MemoryClient
from utils.model import  llm
import os
from dotenv import load_dotenv
import uuid  
from fastapi.responses import ORJSONResponse
import agentops
load_dotenv(override=True) 
os.environ["GEMINI_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ["MEM0_API_KEY"] = os.getenv("MEM0_API_KEY")
os.environ['GRPC_ENABLE_FORK_SUPPORT'] = '0'
os.environ['GRPC_POLL_STRATEGY'] = 'epoll1'


client = MemoryClient()
agentops.init(api_key=os.getenv("AGENTOPS_API_KEY"), default_tags=["Portfolio-Chatbot"] ,skip_auto_end_session=True)


app = FastAPI(
    title="Portfolio Chatbot API",
    description="API for Othman's Portfolio Chatbot",
    version="1.0.0",
    default_response_class=ORJSONResponse
)

allowed_origins = [
    "https://www.0thman.tech" ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
    expose_headers=["Set-Cookie"],
)


crew = Crew(
    agents=[all_repos_agent, about_repo_agent, general_agent, agent_sender, agent_manager],
    tasks=[task_manager],
    process=Process.sequential,
    verbose=False, # i let it jsut  to  see the  logs in the server side
    # manager_llm=llm,
    # manager_agent=agent_manager,
    # output_log_file="./logs/logs.json",
    planning=True,
    planning_llm=llm,
)

def is_greeting(text: str) -> bool:
    greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening", "hi there", "hello there", "salam", "marhba"]
    return any(text.lower().strip().startswith(greeting) for greeting in greetings)

def is_goodbye(text: str) -> bool:
    goodbyes = ["bye", "goodbye", "see you", "see ya", "bslama", "beslama", "au revoir"]
    return any(text.lower().strip().startswith(goodbye) for goodbye in goodbyes)

@app.get("/health")
async def health_check():
    return {"message": "fen a 3chiri hh"}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: Request, chat_request: ChatRequest, response: Response):
    try:
        if is_greeting(chat_request.question):
            return ChatResponse(response="Hi there! I'm your portfolio assistant. How can I help you today?")
        
        if is_goodbye(chat_request.question):
            return ChatResponse(response="Goodbye! Have a great day! Feel free to come back if you have more questions.")

        # print("h1")
        user_id = request.cookies.get("user_id")
        # print("this  is :")
        # print(user_id)
        # print("h2")

        if not user_id:
                    user_id = str(uuid.uuid4())
                    response.set_cookie(
                        key="user_id",
                        value=user_id,
                        httponly=True, 
                        max_age=259200,  # 3 days
                        path="/",
                        samesite="none",
                        secure=True                    )
                    # print(f"New user assigned ID: {user_id}")
        else:
            # print(f"Existing user ID from cookie: {user_id}")
            pass

        all_memories = client.get_all(user_id=user_id,   output_format="v1.1")
        # print(all_memories)
        memory = get_first_10_memories(all_memories)
        # print(f"Memory for user {user_id}: {memory}")
        crew_response = crew.kickoff(inputs={
            "question": chat_request.question,
            "chat history": memory,
        })
        # print("h4")
        # print("user question :" + chat_request.question)
        # print("response from crew : " + crew_response["response"])
        # print("typeeeeeeeeeee : " + str(type(user_id)) )
        # print("id " + user_id)
        # print(client)
        messages = [
            {"role": "user", "content": chat_request.question},
            {"role": "assistant", "content": crew_response["response"]}
        ]
        
        client.add(messages, user_id=user_id,output_format="v1.1")

        return ChatResponse(response=crew_response["response"])

    except Exception as e:
        # print(e)
        # print(e.with_traceback())
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/chat-history/{user_id}")
async def get_chat_history(user_id: str):
    try:        
        all_memories = client.get_all(user_id=user_id, output_format="v1.1")
        return {"history": all_memories}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app, host="0.0.0.0", port=8000 , reload=True)
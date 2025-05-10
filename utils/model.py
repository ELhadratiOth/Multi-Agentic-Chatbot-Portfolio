from crewai import LLM
# from langchain_google_genai import GoogleGenerativeAI
# import os

llm=LLM(
        model="gemini/gemini-2.0-flash",
        temperature=0,
        verbose=True,    
        )
planner=LLM(
        model="gemini/gemini-2.5-flash-preview-04-17",
        temperature=0,
        verbose=True,    
        )

# llm_lang = GoogleGenerativeAI(
#     model="gemini-2.0-flash",
#     temperature=0,
#     google_api_key=os.getenv("GOOGLE_API_KEY_2"),
# )

from pydantic import BaseModel , Field 
from typing  import List


#  repo_data = {
#                     "name of the repository": repo.get("name"),
#                     "Url of the repository": repo.get("html_url"),
#                     "Creation Date": repo.get("created_at")
#                 }
 


class Repository(BaseModel):

    name: str = Field(..., description="The name of the repository")
    url: str = Field(..., description="The public URL of the repository")
    creation_date: str = Field(..., description="The creation date of the repository in ISO format")

class GitHubRepositories(BaseModel):
    repositories: List[Repository] = Field(..., description="Contains all repositories of the user")

class GithubRepoDetails(BaseModel):
    project_details: str = Field(..., description="The README file content with project informations")
    
    
class CrewResponse(BaseModel):
    response:str = Field(...,description="the response of the user question")
    

class ChatRequest(BaseModel):
    question: str = Field(...)

class ChatResponse(BaseModel):
    response: str = Field(...)
    status: str = "success"



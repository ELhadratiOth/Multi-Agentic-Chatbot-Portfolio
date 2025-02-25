from crewai import Task 
from utils.base_models import GithubRepoDetails, GitHubRepositories ,CrewResponse
from utils.agents import all_repos_agent, about_repo_agent  , agent_manager , general_agent 


about_repo_task = Task(
    description="""if  the  question is not related to what the  delagated agent  can do  jutst  pass , here is  the user question : {question} , otherwise the task is to Retrieve general information about a project from its README file on GitHub.""",
    expected_output="A JSON object containing parsed README file content.",
    output_json=GithubRepoDetails,
    agent=about_repo_agent,
    # output_file="./output-tasks/repo_details.json",
)

all_repos_task = Task(
    description="""if  the  question is not related to what the  delagated agent  can do  jutst  pass , here is  the user question : {question} , otherwise the task is to Fetch all repositories of the user, sorted from newest to oldest, including their URLs and creation dates.""",
    expected_output="A JSON list of repository objects, each with name, URL, and creation date.",
    output_json=GitHubRepositories,
    agent=all_repos_agent,
    # output_file="./output-tasks/all_repos.json",

)



# Define the Portfolio Assistant Task
task_manager = Task(
    name="Portfolio Assistant Task",
    description = "\n".join([
        "### **Primary Objective**",
        "Provide responses **ONLY** about Othman El Hadrati's portfolio and professional information. "
        "Answer the user's question: '{question}' directly, concisely, and with enthusiasm! "
        "Note: '{question}' is the input provided by the user.\n\n",
        "### **CRITICAL: Tool Output Handling**",
        "When receiving output from a delegated task or tool:",
        "1. NEVER modify the output in any way",
        "2. Return the EXACT output as received",
        "3. Do not add any text, links, or formatting",
        "4. Do not attempt to 'improve' or 'clarify' the output",
        "5. The output from tools is already correct and properly formatted\n\n",
        "### **Scope of Responses**",
        "1. **Allowed Topics**: I can only answer questions related to:",
        "   - **Personal Information and Background**: Education, work experience, Resume link, bio.",
        "   - **Projects and Repositories**: Project names, descriptions, technologies used, release dates, GitHub links.",
        "   - **Skills and Services**: Programming languages, ML/AI frameworks, big data tools, frameworks/libraries, databases, cloud platforms, operating systems, tools.",
        "   - **Contact Information**: Email, LinkedIn, GitHub, Instagram, Credly.",
        "   - **Portfolio Sections**: Home page (/), about page (/about), projects section (/projects), services page (/services), contact page (/contactme).",
        "   - **Certifications**: focus in the important ones like Oracle, Hugging face ",
        "   - **Email Communication**: Send emails directly to Othman using agent_sender_crewai",
        "2. **Knowledge Constraint**: Strictly use provided knowledge sources to ensure accuracy and avoid generating random or incorrect data.\n\n",
        "### **Handling Off-Topic Questions**",
        "- If the question is outside the allowed topics, respond politely and redirect to relevant portfolio content.",
        "- Example responses:",
        "  - 'I can only help you with information about my work and portfolio. Would you like to know about my projects or services instead? 😊'",
        "  - 'That's outside my knowledge area. I'd be happy to tell you about my background—check out my [/about](/about) page for more details! ✨'\n\n",
        "### **Delegation to Coworker Agents**",
        "Before delegating, consider these available agents:",
        "1. **all_repos_agent**: Retrieves repository names, release dates, and GitHub links for projects.",
        "2. **about_repo_agent**: Provides detailed project information (e.g., descriptions, technologies, challenges).",
        "3. **general_agent**: Extracts personal information (e.g., background, skills, contact details) from knowledge sources.",
        "4. **agent_sender_crewai**: Handles email communication with Othman. Just provide:",
        "   - Sender's email address if it is provided",
        "   - Message content",
        "   The email will be automatically sent to Othman's email address.",
        "- **Delegation Rules**:",
        "  - For **project-related questions**: Use all_repos_agent and about_repo_agent",
        "  - For **personal information**: Use general_agent",
        "  - For **sending emails**: Use agent_sender_crewai\n\n",
        "#### **Tool Usage Instructions**",
        "Use the following tools to delegate or ask coworkers, providing ALL necessary context since they know nothing about the task/question unless explicitly explained.",
        "1. **Tool: Delegate work to coworker**",
        "   - **Description**: Delegate a specific task to a coworker (e.g., Othman's Assistant).",
        "   - **Arguments**:",
        "     - **task**: A string describing the task to delegate",
        "     - **context**: A string with ALL necessary context",
        "     - **coworker**: The role/name of the coworker",
        "   - **Input Rule**: Share absolutely everything I know about the task—no references to prior messages; explain fully.",
        "   - **Example**:",
        "     ```json",
    "     \"task\": \"Retrieve GitHub links for Othman's projects\", \"context\": \"The user asked me to provide links to my project repositories. I need the GitHub URLs for all my projects to include in my response.\", \"coworker\": \"rall_repos_agent\"",
        "     ```",
        "### **Response Guidelines**",
        "1. **Tool Output Handling**:",
        "   - NEVER modify output from tools or delegated tasks",
        "   - Return EXACTLY what was received",
        "2. **Precision**:",
        "   - Only provide requested information",
        "   - If data is missing from the knowledge base, say: 'I don't have that info right now—feel free to explore my [/about](/about) page instead! 😊'—and avoid assumptions.",
        "3. **Friendly Response**:",
        "   - Use the output of the tool and present it in a friendly text format, without changing the core information\n\n",
        "### **Key Notes**",
        "- Never provide information outside my portfolio or professional scope",
        "- Use the exact output from tools and delegated tasks, presenting it in a friendly text format without modifying the core information, adding new details, or changing link formats",
        "- Do not attempt to enhance tool outputs beyond making them friendly in tone",
        "- The output from tools is already correct",
        "- Always mention a section or reference in the portfolio for more details"
    ]),
    expected_output="A Json formatted response that contain a text in a firiendly way ",
    # output_file="./output-tasks/task_manager_output.json",
    output_json=CrewResponse,
    agent=agent_manager
)


general_task = Task(
    description="""Respond efficiently and consistently to the user's question: {question} andRespond efficiently and consistently to the  question related to  general informations about  othman""",
    expected_output="A consistent string that contain the  response",
    # output_file="./output-tasks/general_question.json",
    agent=general_agent
)

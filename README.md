# Portfolio Chatbot API

A sophisticated AI-powered chatbot API that serves as an interactive interface for my portfolio website. Built with FastAPI and CrewAI's intelligent agents, it provides dynamic responses about my projects, skills, and professional background through a coordinated multi-agent system.

## Overview

This chatbot leverages multiple specialized AI agents to deliver comprehensive and context-aware responses about my portfolio. It maintains conversation history and provides personalized interactions using advanced memory management.

## Key Features

- **Multi-Agent Architecture**
  - General Information Agent for personal details and background
  - Repository Agent for GitHub project information
  - About Repository Agent for detailed project insights
  - Agent Manager for coordinating responses

- **Smart Memory Management**
  - Conversation context preservation
  - User interaction history
  - Personalized response generation

- **Secure API Design**
  - FastAPI-based REST endpoints  
  - CORS protection  
  - Environment-based configuration  
  - Cookie-based session management 

- **Email Integration**
  - Gmail API integration for automated communications
  - Secure email sending capabilities
  - Template-based email formatting

## Tech Stack

- **Backend Framework**: FastAPI
- **AI Framework**: CrewAI and LangChain
- **Embedding Model**: Google Text Embedding
- **Memory Storage**: Mem0
- **Language**: Python 3.x
- **Email Service**: Gmail API
- **Version Control**: GitHub API
- **Monitoring**: AgentOps

## Setup

1. **Environment Variables**
   ```
   GOOGLE_API_KEY=your_google_api_key
   MEM0_API_KEY=your_mem0_api_key
   GEMINI_API_KEY=your_gemini_api_key
   GITHUB_TOKEN=your_github_token
   GOOGLE_API_KEY_2=your_gemini_api_key
   AGENTOPS_API_KEY=your_agentips_api_key
   GMAIL_SERVICE_ACCOUNT=your_base64_encoded_service_account_json
   ```

2. **Installation**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the API**
   ```bash
   uvicorn api:app --host 0.0.0.0 --port 8000
   ```

## Deployment

### Server Requirements
- Python 3.x
- 2GB RAM minimum
- Sufficient disk space for dependencies
- HTTPS capability for secure communication

### Deployment Steps

1. **Prepare Environment Variables**
   - Convert your Gmail service account JSON to base64 and set it as `GMAIL_SERVICE_ACCOUNT`
   - Set all other required environment variables
   - Ensure all API keys are properly configured

2. **Server Setup**
   ```bash
   # Clone the repository
   git clone https://github.com/yourusername/PortFolioChatbot.git
   cd PortFolioChatbot

   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt

   # Start the server
   uvicorn api:app --host 0.0.0.0 --port 8000 --workers 4
   ```

3. **Security Considerations**
   - Configure CORS settings in `api.py` for your domain
   - Use HTTPS for all communications
   - Keep API keys and credentials secure
   - Regularly update dependencies

4. **Monitoring**
   - Set up logging for tracking API usage
   - Monitor memory usage and performance
   - Configure error notifications

5. **Maintenance**
   - Regularly backup configuration
   - Update API keys before expiration
   - Monitor service account permissions

### Docker Deployment (Alternative)

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

```bash
# Build and run with Docker
docker build -t portfolio-chatbot .
docker run -p 8000:8000 --env-file .env portfolio-chatbot
```

### Deployment on Render

#### Prerequisites
- A Render account
- Your repository pushed to GitHub
- All required API keys and credentials

#### Deployment Steps

1. **Prepare Your Environment Variables**
   - Convert your Gmail service account JSON to base64:
     ```bash
     base64 -w 0 logs/token.json > service_account_base64.txt
     ```
   - Copy the output to use as `GMAIL_SERVICE_ACCOUNT` in Render

2. **Deploy on Render**
   - Log in to your Render dashboard
   - Click "New +" and select "Web Service"
   - Connect your GitHub repository
   - Fill in the following settings:
     - **Name**: `portfolio-chatbot` (or your preferred name)
     - **Environment**: `Python`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn api:app --host 0.0.0.0 --port $PORT`

3. **Configure Environment Variables**
   In your Render dashboard, add the following environment variables:
   ```
   GOOGLE_API_KEY=your_google_api_key
   MEM0_API_KEY=your_mem0_api_key
   GEMINI_API_KEY=your_gemini_api_key
   GITHUB_TOKEN=your_github_token
   GOOGLE_API_KEY_2=your_gemini_api_key
   AGENTOPS_API_KEY=your_agentips_api_key
   GMAIL_SERVICE_ACCOUNT=your_base64_encoded_service_account_json
   ```

4. **Deploy**
   - Click "Create Web Service"
   - Render will automatically build and deploy your application
   - Your API will be available at `https://your-app-name.onrender.com`

#### Important Notes
- Render's free tier has some limitations on memory and CPU
- The service may take a few minutes to start up initially
- Configure your frontend to use the new Render URL
- Update CORS settings in `api.py` to allow your domain

## API Endpoints

- `GET /health`
  - Health check endpoint
  - Returns API status

- `POST /chat`
  - Main chat interaction endpoint
  - Accepts chat messages and returns AI responses

- `GET /chat/history/{user_id}`
  - Retrieves chat history for a specific user

## Project Structure

```
PrortFolioChatbot/
├── api.py                 # Main FastAPI application and endpoints
├── .env.sample           # Sample environment variables template
├── requirements.txt      # Project dependencies
│
├── utils/               # Core utility modules
│   ├── agents.py        # AI agent definitions and configurations
│   ├── tasks.py         # Task management and orchestration
│   ├── tools.py         # Utility functions and helper tools
│   ├── base_models.py   # Pydantic data models
│   ├── knowledge.py     # Knowledge base management
│   └── model.py         # AI model configurations
│
├── knowledge/          # Knowledge base storage
|   ├── My_RESUME.pdf   # Resume 
│   └── general_data/   # Portfolio-related knowledge
│
├── memory/            # Conversation memory storage
│   └── long_term_memry/       # User chat history
│
├── tests/             # Test suite
│   
└── logs/             # Application logs

```

### Architecture Overview

The project follows a modular architecture with several key components:

1. **API Layer** (`api.py`)
   - FastAPI application setup
   - Endpoint definitions
   - CORS middleware
   - Request/Response handling

2. **Agent System** (`utils/agents.py`)
   - Built-in caching and delegation capabilities
   - Google Text Embedding integration
   - General Information Agent: Handles personal and background info
   - Repository Agent: Manages GitHub project data
   - About Repository Agent: Provides detailed project insights
   - Agent Manager: Orchestrates agent interactions

3. **Task Management** (`utils/tasks.py`)
   - Task definition and scheduling
   - Agent task assignment
   - Task execution flow
   - Response processing
   - Specialized task handlers for different information types

4. **Data Models** (`utils/base_models.py`)
   - Repository: GitHub repository structure
   - ChatRequest: Incoming chat message format
   - ChatResponse: Outgoing response format
   - CrewResponse: Agent response structure

5. **Knowledge Management**
   - Portfolio information storage
   - Structured data organization
   - Knowledge base access patterns

6. **Memory System**
   - Chat history persistence
   - Context management
   - User session tracking

7. **Tools and Utilities** (`utils/tools.py`)
   - GitHub API integration for repository management
   - Gmail API integration for email communications
   - Data transformation helpers
   - Utility functions
   - Repository content retrieval

### Data Flow

1. User sends a question via the chat endpoint
2. Request is validated using Pydantic models
3. Agent Manager assigns the task to appropriate agent(s)
4. Agents access knowledge base , memory, or by  using  the appropriate tool as needed
5. Response is generated and formatted
6. Chat history is updated
7. Response is returned to user

### Integration Points

- **Frontend**: Portfolio website (https://www.0thman.tech)
- **External Services**:
  - GitHub API for repository data
  - Google Text Embedding API
  - Mem0 for memory management
  - Gemini API for AI model
  - Gmail API for email communications

## Security

- CORS configuration limited to portfolio domain
- Secure API key management
- Request validation and sanitization

## Integration

This API is designed to integrate seamlessly with my portfolio website at https://www.0thman.tech, providing visitors with an interactive way to learn about my professional experience and projects.

## Contributing

Feel free to open issues or submit pull requests if you find any bugs or have suggestions for improvements.

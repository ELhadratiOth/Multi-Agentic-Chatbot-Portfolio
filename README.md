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
   ```

2. **Installation**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the API**
   ```bash
   uvicorn api:app --host 0.0.0.0 --port 8000
   ```

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


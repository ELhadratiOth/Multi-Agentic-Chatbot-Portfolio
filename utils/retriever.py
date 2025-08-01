import os
from langchain_qdrant import QdrantVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from qdrant_client import QdrantClient
from dotenv import load_dotenv
from pydantic import Field
from crewai.tools import tool


# Load environment variables
load_dotenv(override=True)

# Validate environment variables
url = os.getenv("QDRANT_URL")
api_key = os.getenv("QDRANT_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")

if not all([url, api_key, google_api_key]):
    # logger.error("Missing environment variables: QDRANT_URL, QDRANT_API_KEY, or GOOGLE_API_KEY")
    raise ValueError("Required environment variables are not set")

# Initialize embeddings
try:
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        task_type="semantic_similarity",
        google_api_key=google_api_key
    )
except Exception as e:
    print(f"Failed to initialize embeddings: {str(e)}")
    raise

# Initialize Qdrant client
try:
    qdrant_client = QdrantClient(
        url=url,
        api_key=api_key,
        prefer_grpc=True
    )
except Exception as e:
    print(f"Failed to initialize Qdrant client: {str(e)}")
    raise

# Initialize vector store
try:
    vector_store = QdrantVectorStore(
        client=qdrant_client,
        collection_name="portfolio_data",
        embedding=embeddings
    )
except Exception as e:
    print(f"Failed to initialize Qdrant vector store: {str(e)}")
    raise

# Initialize retriever
retriever = vector_store.as_retriever(search_kwargs={"k": 8})

@tool
def general_info_retriever(query: str = Field(
    description="A query about general information about Othman El Hadrati (use affirmative form, e.g., 'Othman's certifications' instead of 'What are Othman's certifications?')"
)) -> str:
    """
    Uses semantic search to retrieve responses for static questions about general information about Othman El Hadrati.

    Args:
        query (str): The query to perform. Use the affirmative form rather than a question.

    Returns:
        str: A string containing retrieved document snippets and metadata relevant to the query.

    Raises:
        ValueError: If the query is empty or invalid.
        RuntimeError: If retrieval fails due to vector store issues.
    """
    # Validate query
    if not query or not isinstance(query, str):
        print("Invalid or empty query provided")
        raise ValueError("Query must be a non-empty string")

    

    try:
        # Invoke retriever
        docs = retriever.invoke(query)
        if not docs:
            print(f"No documents found for query: {query}")
            return f"No relevant information found for query: {query}"

        # Format output with content and metadata
        result = "\nAccurate documents:\n"
        for i, doc in enumerate(docs, 1):
            result += f"\n===== Document {i} =====\n"
            result += f"Content: {doc.page_content}\n"
            result += f"Metadata: {doc.metadata}\n"

        print(f"Successfully retrieved {len(docs)} documents for query: {query}")
        return result

    except Exception as e:
        print(f"Failed to retrieve documents for query '{query}': {str(e)}")
        raise RuntimeError(f"Retrieval failed: {str(e)}")
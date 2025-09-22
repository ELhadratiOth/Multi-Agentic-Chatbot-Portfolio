import os
import json
import logging
from langchain_community.document_loaders import JSONLoader
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_qdrant import FastEmbedSparse, RetrievalMode
from langchain.docstore.document import Document

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv(override=True)

# Validate environment variables
url = os.getenv("QDRANT_URL")
api_key = os.getenv("QDRANT_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")

if not all([url, api_key, google_api_key]):
    logger.error("Missing environment variables: QDRANT_URL, QDRANT_API_KEY, or GOOGLE_API_KEY")
    raise ValueError("Required environment variables are not set")

# Initialize embeddings
try:
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        task_type="semantic_similarity",
        google_api_key=google_api_key
    )
    sparse_embeddings = FastEmbedSparse(model_name="Qdrant/bm25")
except Exception as e:
    logger.error(f"Failed to initialize embeddings: {str(e)}")
    raise

# Function to convert experiences JSON data to chunks and metadata
def experiences_to_chunks(data):
    chunks = []
    metadata = []
    
    try:
        for experience in data['experiences']:
            # Main experience info
            exp_content = (f"Position: {experience['position']}, Company: {experience['company']}, "
                          f"Job Type: {experience['jobType']}, Location: {experience['location']}, "
                          f"Duration: {experience['duration']}, Description: {experience['description']}")
            chunks.append(exp_content)
            metadata.append({
                "category": "experiences", 
                "subcategory": "work_experience", 
                "id": f"experience_{experience['id']}",
                "links": [], 
                "source": "experiences", 
                "timestamp": "2025-05-11",
                "company": experience['company'],
                "position": experience['position']
            })
            
            # Responsibilities
            if 'responsibilities' in experience:
                resp_content = f"Responsibilities at {experience['company']}: " + "; ".join(experience['responsibilities'])
                chunks.append(resp_content)
                metadata.append({
                    "category": "experiences", 
                    "subcategory": "responsibilities", 
                    "id": f"experience_resp_{experience['id']}",
                    "links": [], 
                    "source": "experiences.responsibilities", 
                    "timestamp": "2025-05-11",
                    "company": experience['company'],
                    "position": experience['position']
                })
            
            # Tools/Technologies
            if 'tools' in experience:
                tools_content = f"Tools and Technologies used at {experience['company']}: {', '.join(experience['tools'])}"
                chunks.append(tools_content)
                metadata.append({
                    "category": "experiences", 
                    "subcategory": "tools_technologies", 
                    "id": f"experience_tools_{experience['id']}",
                    "links": [], 
                    "source": "experiences.tools", 
                    "timestamp": "2025-05-11",
                    "company": experience['company'],
                    "position": experience['position']
                })
                
    except KeyError as e:
        logger.error(f"Missing key in experiences JSON data: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error processing experiences JSON data: {str(e)}")
        raise
    
    return chunks, metadata

# Function to convert projects JSON data to chunks and metadata
def projects_to_chunks(data):
    chunks = []
    metadata = []
    
    try:
        for project in data['projects']:
            # Main project info
            project_content = (f"Project: {project['serviceName']}, Tools: {', '.join(project['tools'])}, "
                              f"Type: {project['project_type']}, Link: {project['link']}")
            chunks.append(project_content)
            metadata.append({
                "category": "projects", 
                "subcategory": project['project_type'], 
                "id": f"project_{project['id']}",
                "links": [project['link']] if project['link'] else [], 
                "source": "projects", 
                "timestamp": "2025-05-11",
                "project_type": project['project_type'],
                "service_name": project['serviceName']
            })
                
    except KeyError as e:
        logger.error(f"Missing key in projects JSON data: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error processing projects JSON data: {str(e)}")
        raise
    
    return chunks, metadata

# Function to convert JSON data to chunks and metadata
def json_to_chunks(data):
    chunks = []
    metadata = []

    try:
        # Personal Info
        chunks.append(f"Name: {data['personal_info']['name']}, Location: {data['personal_info']['location']}, "
                      f"Role: {data['personal_info']['role']}, Bio: {data['personal_info']['bio']}")
        metadata.append({"category": "personal_info", "subcategory": "basic_details", "id": "personal_info_1",
                         "links": [], "source": "personal_info", "timestamp": "2025-05-11"})

        chunks.append(f"Education: {data['personal_info']['education']['institution']}, "
                      f"Program: {data['personal_info']['education']['program / speciality']}, "
                      f"Year: {data['personal_info']['education']['year']}")
        metadata.append({"category": "personal_info", "subcategory": "education", "id": "personal_info_2",
                         "links": [], "source": "personal_info.education", "timestamp": "2025-05-11"})

        social_links = ", ".join([f"{k}: {v}" for k, v in data['personal_info']['social_media links'].items()])
        chunks.append(f"Social Media Links: {social_links}")
        social_links_list = list(data['personal_info']['social_media links'].values())
        metadata.append({"category": "personal_info", "subcategory": "social_media", "id": "personal_info_3",
                         "links": social_links_list, "source": "personal_info.social_media_links", "timestamp": "2025-05-11"})

        chunks.append(f"Resume: {data['personal_info']['RESUME / CV']['link']}")
        metadata.append({"category": "personal_info", "subcategory": "resume", "id": "personal_info_4",
                         "links": [data['personal_info']['RESUME / CV']['link']],
                         "source": "personal_info.RESUME / CV", "timestamp": "2025-05-11"})

        # Skills
        for skill_type, skills in data['skills'].items():
            chunks.append(f"Skills - {skill_type.replace('_', ' ').title()}: {', '.join(skills)}")
            metadata.append({"category": "skills", "subcategory": skill_type, "id": f"skills_{skill_type}",
                             "links": [], "source": f"skills.{skill_type}", "timestamp": "2025-05-11"})

        # Services
        for i, service in enumerate(data['services'], 1):
            chunks.append(f"Service: {service['name']}, Description: {service['description']}")
            metadata.append({"category": "services", "subcategory": "service", "id": f"services_{i}",
                             "links": [], "source": "services", "timestamp": "2025-05-11"})

        # Certifications
        for i, cert in enumerate(data['certifications']['important and relevant certifications'], 1):
            chunks.append(f"Certification: {cert['name']}, Provider: {cert['provider']}, Date: {cert['date']}, "
                          f"Link: {cert['link']}")
            metadata.append({"category": "certifications", "subcategory": "important_certifications",
                             "id": f"certifications_important_{i}", "links": [cert['link']],
                             "source": "certifications.important_certifications", "timestamp": "2025-05-11"})

        for i, cert in enumerate(data['certifications']['simple certifications'], 1):
            chunks.append(f"Certification: {cert['name']}, Provider: {cert['provider']}, Date: {cert['date']}, "
                          f"Link: {cert['link']}")
            metadata.append({"category": "certifications", "subcategory": "simple_certifications",
                             "id": f"certifications_simple_{i}", "links": [cert['link']],
                             "source": "certifications.simple_certifications", "timestamp": "2025-05-11"})

        # Portfolio Routes
        for route, details in data['portfolio_routes'].items():
            chunks.append(f"Portfolio Route: {route.title()}, Path: {details['path']}, "
                          f"Description: {details['description']}")
            metadata.append({"category": "portfolio_routes", "subcategory": route, "id": f"portfolio_routes_{route}",
                             "links": [], "source": f"portfolio_routes.{route}", "timestamp": "2025-05-11"})

        # Contact Methods
        chunks.append(f"Contact Email: {data['contact_methods']['email']['primary']}, "
                      f"Response: {data['contact_methods']['email']['response']}")
        metadata.append({"category": "contact_methods", "subcategory": "email", "id": "contact_methods_1",
                         "links": [data['contact_methods']['email']['primary']],
                         "source": "contact_methods.email", "timestamp": "2025-05-11"})

        chunks.append(f"Contact Form: Location: {data['contact_methods']['contact_form']['location']}, "
                      f"Response: {data['contact_methods']['contact_form']['response']}")
        metadata.append({"category": "contact_methods", "subcategory": "contact_form", "id": "contact_methods_2",
                         "links": [], "source": "contact_methods.contact_form", "timestamp": "2025-05-11"})

        # FAQs
        for i, faq in enumerate(data['frequently_asked_questions'], 1):
            chunks.append(f"FAQ: {faq['question']}, Answer: {faq['answer']}")
            metadata.append({"category": "frequently_asked_questions", "subcategory": "faq", "id": f"faq_{i}",
                             "links": [], "source": "frequently_asked_questions", "timestamp": "2025-05-11"})

    except KeyError as e:
        logger.error(f"Missing key in JSON data: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error processing JSON data: {str(e)}")
        raise

    return chunks, metadata

# Load and process JSON files
all_documents = []

# Process general_data.json
try:
    with open("general_data.json", "r") as f:
        general_data = json.load(f)
    chunks, metadata = json_to_chunks(general_data)
    general_documents = [Document(page_content=chunk, metadata=meta) for chunk, meta in zip(chunks, metadata)]
    all_documents.extend(general_documents)
    logger.info(f"Processed general_data.json: {len(general_documents)} documents")
except FileNotFoundError:
    logger.error("JSON file 'general_data.json' not found")
    raise
except json.JSONDecodeError:
    logger.error("Invalid JSON format in 'general_data.json'")
    raise

# Process experiences.json
try:
    with open("experiences.json", "r") as f:
        experiences_data = json.load(f)
    chunks, metadata = experiences_to_chunks(experiences_data)
    experience_documents = [Document(page_content=chunk, metadata=meta) for chunk, meta in zip(chunks, metadata)]
    all_documents.extend(experience_documents)
    logger.info(f"Processed experiences.json: {len(experience_documents)} documents")
except FileNotFoundError:
    logger.warning("JSON file 'experiences.json' not found, skipping...")
except json.JSONDecodeError:
    logger.error("Invalid JSON format in 'experiences.json'")
    raise

# Process projects.json
try:
    with open("projects.json", "r") as f:
        projects_data = json.load(f)
    chunks, metadata = projects_to_chunks(projects_data)
    project_documents = [Document(page_content=chunk, metadata=meta) for chunk, meta in zip(chunks, metadata)]
    all_documents.extend(project_documents)
    logger.info(f"Processed projects.json: {len(project_documents)} documents")
except FileNotFoundError:
    logger.warning("JSON file 'projects.json' not found, skipping...")
except json.JSONDecodeError:
    logger.error("Invalid JSON format in 'projects.json'")
    raise

logger.info(f"Total documents to store: {len(all_documents)}")

# Create LangChain Documents
documents = all_documents

# Initialize Qdrant client
try:
    qdrant_client = QdrantClient(
        url=url,
        api_key=api_key,
        prefer_grpc=True
    )
except Exception as e:
    logger.error(f"Failed to initialize Qdrant client: {str(e)}")
    raise

# Store documents in Qdrant
try:
    QdrantVectorStore.from_documents(
        documents=documents,
        embedding=embeddings,
        sparse_embedding=sparse_embeddings,
        url=url,
        api_key=api_key,
        collection_name="portfolio_data",
        retrieval_mode=RetrievalMode.HYBRID,
        force_recreate=True,  # Recreate collection for fresh data
        prefer_grpc=True
    )
    logger.info("Data saved successfully to Qdrant!")
except Exception as e:
    logger.error(f"Failed to save data to Qdrant: {str(e)}")
    raise
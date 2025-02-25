from crewai.crew import Knowledge
from crewai.knowledge.source.json_knowledge_source import JSONKnowledgeSource
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource

knowledges = []

# Create a JSON knowledge source with updated metadata
json_source = JSONKnowledgeSource(
    file_paths=["../knowledge/general_data.json"],
    chunk_size=4000,
    chunk_overlap=200,
    metadata={
        "source_type": "JSON",
        "description": "Personal and professional data of Othman El Hadrati",
        "author": "Othman El Hadrati",
        "location": "Kenitra, Morocco",
        "role": "Data and Software Engineering Student",
        "education": "National School of Applied Sciences in Al Hoceima (ENSAH)",
        "RESUME / CV":"resume link of othman",
        "skills": [
            "HTML5", "CSS3", "JavaScript", "Java", "Python", "C",
            "Machine Learning", "Natural Language Processing", "Big Data",
            "React", "FastAPI", "AWS", "SQL", "NoSQL", "Docker" , "Generative AI"
        ],
        "services": ["Data Engineering", "Machine Learning", "Web Development", "Cloud Solutions", "Hosting", "Problem Solving", "Database Management"],
    }
)
knowledges.append(json_source)

# Create a PDF knowledge source with detailed metadata as before
pdf_source = PDFKnowledgeSource(
    file_paths=["../knowledge/MY_RESUME.pdf"],
    chunk_size=500,
    chunk_overlap=20,
    metadata={
        "description": "Resume of Othman El Hadrati - Data and Software Engineering Student",
        "author": "Othman El Hadrati",
        "location": "Kenitra, Morocco",
        "education": "National School of Applied Sciences in Al Hoceima (ENSAH)",
        "skills": [
            "Python", "Java", "JavaScript", "React", "FastAPI", "SQL", "NoSQL", 
            "Machine Learning", "NLP", "Big Data", "AWS", "Docker"
        ],
       
    }
)

knowledges.append(pdf_source)
import asyncio
import logging
import sys
from pathlib import Path

# Load environment variables
from dotenv import load_dotenv

load_dotenv()
from google.adk.plugins.logging_plugin import LoggingPlugin
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Add src to python path
sys.path.append(str(Path(__file__).parent / "src"))

from cv_enhancer.agents.cv_enhancer_flow.agent import root_agent
from cv_enhancer.agents.cv_enhancer_flow.tools.rag import ingest_resume, init_db
from cv_enhancer.schemas import JsonResume

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

JOB_OFFER_TEXT = """
We are looking for a Senior Python Developer to join our team.
The ideal candidate should have experience with:
- Python 3.10+
- Django and FastAPI
- Cloud platforms (AWS or GCP)
- Containerization (Docker, Kubernetes)
- CI/CD pipelines
- Machine Learning basics is a plus

Responsibilities:
- Design and implement scalable backend services
- Collaborate with frontend developers
- Write clean, testable code
"""

async def main():
    # Initialize the database (mock or real)
    # For this test, we might need a real resume file or mock the db
    # Let's assume there is a resume.json in data/resume.json
    # If not, we might fail or need to create a dummy one.

    # Ensure data directory exists
    Path("data").mkdir(exist_ok=True)
    resume_path = Path("data/resume.json")
    if not resume_path.exists():
        # Create a dummy resume
        with resume_path.open("w") as f:
            f.write("""
{
  "basics": {
    "name": "John Doe",
    "label": "Programmer",
    "email": "john@gmail.com",
    "phone": "(912) 555-4321",
    "summary": "A summary of John Doe...",
    "location": {
      "address": "2712 Broadway St",
      "postalCode": "CA 94115",
      "city": "San Francisco",
      "countryCode": "US",
      "region": "California"
    },
    "profiles": [{
      "network": "Twitter",
      "username": "john",
      "url": "http://twitter.com/john"
    }]
  },
  "work": [{
    "company": "Company",
    "position": "President",
    "website": "http://company.com",
    "startDate": "2013-01-01",
    "endDate": "2014-01-01",
    "summary": "Description...",
    "highlights": [
      "Started the company"
    ]
  }],
  "volunteer": [{
    "organization": "Organization",
    "position": "Volunteer",
    "website": "http://organization.com/",
    "startDate": "2012-01-01",
    "endDate": "2013-01-01",
    "summary": "Description...",
    "highlights": [
      "Awarded 'Volunteer of the Month'"
    ]
  }],
  "education": [{
    "institution": "University",
    "area": "Software Development",
    "studyType": "Bachelor",
    "startDate": "2011-01-01",
    "endDate": "2013-01-01",
    "gpa": "4.0",
    "courses": [
      "DB1101 - Basic SQL"
    ]
  }],
  "awards": [{
    "title": "Award",
    "date": "2014-11-01",
    "awarder": "Company",
    "summary": "There is no spoon."
  }],
  "publications": [{
    "name": "Publication",
    "publisher": "Company",
    "releaseDate": "2014-10-01",
    "website": "http://publication.com",
    "summary": "Description..."
  }],
  "skills": [{
    "name": "Web Development",
    "level": "Master",
    "keywords": [
      "HTML",
      "CSS",
      "Javascript"
    ]
  }],
  "languages": [{
    "language": "English",
    "fluency": "Native Speaker"
  }],
  "interests": [{
    "name": "Wildlife",
    "keywords": [
      "Ferrets",
      "Unicorns"
    ]
  }],
  "references": [{
    "name": "Jane Doe",
    "reference": "Reference..."
  }]
}
            """)

    # Initialize DB
    init_db("resume")

    # Load and ingest resume
    with resume_path.open("r") as f:
        json_resume = JsonResume.model_validate_json(f.read())

    ingest_result = ingest_resume(json_resume)
    logger.info(f"Ingest result: {ingest_result}")

    session_service = InMemorySessionService()

    runner = Runner(
        agent=root_agent,
        app_name="cv_enhancer_app",
        session_service=session_service,
        plugins=[
            LoggingPlugin(),
        ],
    )

    logger.info("✅ Runner created. Starting execution...")

    # Create session
    await session_service.create_session(session_id="test_session", user_id="test_user", app_name="cv_enhancer_app")

    content = types.Content(parts=[types.Part(text=JOB_OFFER_TEXT)])
    async for event in runner.run_async(new_message=content, session_id="test_session", user_id="test_user"):
        logger.info(event)

    logger.info("✅ Execution finished.")

if __name__ == "__main__":
    asyncio.run(main())

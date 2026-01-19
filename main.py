import asyncio
import json
import logging
import sys

from app.config import get_settings, Settings
from app.models import ResumeInput, ResumeScore
from app.services import AIService, AIServiceError
from app.utils import setup_logger, read_prompt_file


MOCK_JOB_TITLE = "Senior Python Developer"

MOCK_JOB_DESCRIPTION = """
We are looking for a Senior Python Developer to join our growing engineering team.
You will be responsible for designing and implementing scalable backend services,
mentoring junior developers, and collaborating with cross-functional teams.
The ideal candidate has strong experience with modern Python frameworks and cloud technologies.
"""

MOCK_REQUIREMENTS = [
    "5+ years of professional Python development experience",
    "Strong experience with FastAPI or Django REST Framework",
    "Proficiency in async Python programming",
    "Experience with PostgreSQL and Redis",
    "Knowledge of AWS services (EC2, S3, Lambda)",
    "Experience with Docker and Kubernetes",
    "Excellent communication and mentoring skills",
    "Bachelor's degree in Computer Science or equivalent",
]

MOCK_RESUME = """
JOHN DOE
Senior Software Engineer | john.doe@email.com | LinkedIn: linkedin.com/in/johndoe

PROFESSIONAL SUMMARY
Experienced software engineer with 6+ years specializing in Python backend development.
Passionate about building scalable microservices and mentoring team members.
Strong advocate for clean code and test-driven development practices.

CURRENT ROLE
Senior Python Developer at TechCorp Inc. (2021 - Present)
- Lead development of microservices architecture using FastAPI and async Python
- Designed and implemented RESTful APIs serving 10M+ daily requests
- Mentored team of 4 junior developers, conducting code reviews and pair programming
- Migrated legacy Django monolith to containerized microservices on AWS EKS
- Technologies: Python 3.11, FastAPI, PostgreSQL, Redis, Docker, Kubernetes, AWS

PREVIOUS EXPERIENCE
Python Developer at StartupXYZ (2019 - 2021)
- Built payment processing system using Django REST Framework
- Implemented event-driven architecture with RabbitMQ
- Improved API response times by 40% through query optimization
- Technologies: Python, Django, PostgreSQL, RabbitMQ, Docker

Junior Developer at WebAgency (2017 - 2019)
- Developed web applications using Python and Flask
- Created automated testing suites with pytest
- Participated in agile sprints and daily standups

EDUCATION
Bachelor of Science in Computer Science
State University (2013 - 2017)
GPA: 3.7/4.0

SKILLS
Languages: Python, JavaScript, SQL, Bash
Frameworks: FastAPI, Django, Flask, SQLAlchemy
Databases: PostgreSQL, Redis, MongoDB
Cloud: AWS (EC2, S3, Lambda, EKS), Docker, Kubernetes
Tools: Git, GitHub Actions, Terraform, Prometheus, Grafana

CERTIFICATIONS
- AWS Certified Solutions Architect - Associate
- Python Institute PCPP - Certified Professional in Python Programming
"""


async def run_analysis(
    settings: Settings,
    logger: logging.Logger,
) -> ResumeScore:
    
    logger.info("Loading scoring prompt from: %s", settings.scoring_prompt_path)
    system_prompt = read_prompt_file(settings.scoring_prompt_path)
    
    ai_service = AIService(
        api_key=settings.openai_api_key,
        model=settings.openai_model,
        temperature=settings.openai_temperature,
        max_tokens=settings.openai_max_tokens,
    )
    
    resume_input = ResumeInput(
        job_title=MOCK_JOB_TITLE,
        job_description=MOCK_JOB_DESCRIPTION,
        requirements=MOCK_REQUIREMENTS,
        resume_text=MOCK_RESUME,
    )
    
    logger.info("Analyzing resume for position: %s", resume_input.job_title)
    
    result = await ai_service.analyze_resume(
        resume_input=resume_input,
        system_prompt=system_prompt,
    )
    
    return result


async def main() -> int:
    
    try:
        settings = get_settings()
    except Exception as e:
        print(f"Failed to load settings: {e}", file=sys.stderr)
        print("Make sure you have a .env file with OPENAI_API_KEY set", file=sys.stderr)
        return 1
    
    logger = setup_logger(
        name="ai_resume_analyzer",
        level=settings.log_level,
    )
    
    logger.info("=" * 60)
    logger.info("🚀 AI Resume Analyzer v1.0.0")
    logger.info("=" * 60)
    logger.info("Model: %s | Temperature: %.2f", settings.openai_model, settings.openai_temperature)
    
    try:
        result = await run_analysis(settings, logger)
        
        print(result.to_summary())
        
        logger.info("Raw JSON output:")
        print("\n📄 JSON Output:")
        print(json.dumps(result.model_dump(), indent=2, ensure_ascii=False))
        
        return 0
        
    except FileNotFoundError as e:
        logger.error("Configuration error: %s", str(e))
        return 1
        
    except AIServiceError as e:
        logger.error("AI Service error: %s", str(e))
        return 1
        
    except Exception as e:
        logger.exception("Unexpected error occurred")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

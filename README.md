# 🤖 AI Resume Analyzer

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![OpenAI GPT-4o](https://img.shields.io/badge/OpenAI-GPT--4o-green.svg)](https://openai.com/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> **A professional resume scoring system powered by OpenAI GPT-4o with structured outputs using Pydantic validation.**

This is a **Clean Room Implementation** portfolio project demonstrating best practices in Python development, AI integration, and software architecture for technical candidate screening.

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [API Reference](#-api-reference)
- [Docker](#-docker)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

- **🎯 Structured AI Outputs**: Uses OpenAI's `beta.chat.completions.parse()` for type-safe responses
- **📊 Comprehensive Scoring**: Evaluates candidates on Hard Skills, Experience, Soft Skills, and Education
- **🔒 Type Safety**: Full Pydantic v2 validation with detailed field descriptions
- **⚡ Async Architecture**: Built with async/await for optimal performance
- **🐳 Docker Ready**: Multi-stage Dockerfile with security best practices
- **📝 Professional Logging**: Structured logging without print statements
- **🔐 Secure Configuration**: Environment-based secrets management

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         main.py                                  │
│                    (Async Entrypoint)                           │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        app/                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  config.py   │  │  models.py   │  │    services.py       │  │
│  │  (Settings)  │  │  (Pydantic)  │  │    (AIService)       │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
│                                               │                  │
│  ┌──────────────────────────────────────────┐│                  │
│  │              utils.py                     ││                  │
│  │    (Logger, File Helpers)                 ││                  │
│  └──────────────────────────────────────────┘│                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     OpenAI GPT-4o API                            │
│              (Structured Outputs with Pydantic)                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛠 Tech Stack

| Category | Technology |
|----------|------------|
| **Language** | Python 3.11+ with strict Type Hints |
| **AI/LLM** | OpenAI GPT-4o with Structured Outputs |
| **Validation** | Pydantic v2 |
| **Configuration** | pydantic-settings + python-dotenv |
| **Async** | asyncio (native) |
| **Logging** | Python logging module |
| **Container** | Docker with multi-stage builds |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- Docker (optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/luiz0ar/ai-resume-analyzer.git
   cd ai-resume-analyzer
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

5. **Run the analyzer**
   ```bash
   python main.py
   ```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | ✅ Yes | - | Your OpenAI API key |
| `OPENAI_MODEL` | No | `gpt-4o` | Model to use for analysis |
| `OPENAI_TEMPERATURE` | No | `0.3` | Temperature (0.0-2.0) |
| `OPENAI_MAX_TOKENS` | No | `2000` | Max tokens in response |
| `LOG_LEVEL` | No | `INFO` | Logging level |
| `PROMPTS_DIR` | No | `prompts` | Prompts directory path |

### Example `.env` file

```env
OPENAI_API_KEY=sk-proj-your-api-key-here
OPENAI_MODEL=gpt-4o
OPENAI_TEMPERATURE=0.3
LOG_LEVEL=INFO
```

---

## 📖 Usage

### Basic Usage

```bash
python main.py
```

### Sample Output

```
============================================================
📊 RESUME ANALYSIS RESULT
============================================================

🎯 SCORE: 87/100

📝 REASONING:
The candidate demonstrates strong alignment with the job requirements...

💪 STRENGTHS:
  ✅ 6+ years of Python experience with focus on FastAPI
  ✅ Strong AWS and Kubernetes experience in current role
  ✅ Proven mentoring and leadership capabilities

⚠️  GAPS:
  ❌ No explicit Redis experience mentioned in current role
  ❌ Limited evidence of system design documentation
  ❌ Could benefit from more open-source contributions
============================================================
```

### Programmatic Usage

```python
import asyncio
from app.config import get_settings
from app.models import ResumeInput
from app.services import AIService
from app.utils import read_prompt_file

async def analyze():
    settings = get_settings()
    
    service = AIService(
        api_key=settings.openai_api_key,
        model=settings.openai_model,
    )
    
    input_data = ResumeInput(
        job_title="Senior Python Developer",
        job_description="...",
        requirements=["Python", "FastAPI", "AWS"],
        resume_text="...",
    )
    
    prompt = read_prompt_file(settings.scoring_prompt_path)
    result = await service.analyze_resume(input_data, prompt)
    
    print(f"Score: {result.score}/100")

asyncio.run(analyze())
```

---

## 📁 Project Structure

```
ai-resume-analyzer/
├── app/
│   ├── __init__.py          # Package initialization
│   ├── config.py            # Settings & environment loading
│   ├── models.py            # Pydantic schemas (ResumeInput, ResumeScore)
│   ├── services.py          # AIService with OpenAI integration
│   └── utils.py             # Logger setup & file helpers
├── prompts/
│   └── scoring_prompt.txt   # System prompt for scoring rubric
├── .env.example             # Environment template
├── .gitignore               # Git ignore rules
├── Dockerfile               # Multi-stage Docker build
├── docker-compose.yaml      # Docker Compose configuration
├── main.py                  # Async entrypoint
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

---

## 📚 API Reference

### Models

#### `ResumeInput`
```python
class ResumeInput(BaseModel):
    job_title: str           # Job position title
    job_description: str     # Detailed job description
    requirements: List[str]  # Required skills list
    resume_text: str         # Candidate's resume text
```

#### `ResumeScore`
```python
class ResumeScore(BaseModel):
    reasoning: str              # Chain of thought explanation
    score: int                  # Score 0-100
    positive_points: List[str]  # Top strengths (3-5 items)
    negative_points: List[str]  # Top gaps (3-5 items)
```

### Services

#### `AIService`
```python
class AIService:
    def __init__(self, api_key: str, model: str = "gpt-4o", ...)
    async def analyze_resume(self, input: ResumeInput, prompt: str) -> ResumeScore
    async def health_check(self) -> bool
```

---

## 🐳 Docker

### Build and Run

```bash
# Build the image
docker build -t ai-resume-analyzer .

# Run with environment variables
docker run --rm \
  -e OPENAI_API_KEY=your-key-here \
  ai-resume-analyzer
```

### Using Docker Compose

```bash
# Create .env file with your API key first
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Run the analyzer
docker-compose up --build

# Run in development mode
docker-compose --profile dev up
```

---

## 👤 Author

**AI Resume Analyzer Team**

- Luiz Felipe Arcanjo Rangel
- Portfolio Project - Clean Room Implementation
- Demonstrates: Python, OpenAI API, Pydantic, Async Programming, Docker

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-blue?logo=linkedin)](https://www.linkedin.com/in/luiz-felipe-arcanjo-rangel-7b9442262/)

---

<p align="center">
  Made with ❤️ and 🐍 Python
</p>

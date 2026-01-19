import logging
from typing import Optional

from openai import AsyncOpenAI, APIError, APIConnectionError, RateLimitError

from app.models import ResumeInput, ResumeScore


logger = logging.getLogger(__name__)


class AIServiceError(Exception):
    pass


class AIService:
    
    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o",
        temperature: float = 0.3,
        max_tokens: int = 2000,
    ) -> None:
        if not api_key or not api_key.strip():
            raise ValueError("OpenAI API key is required")
        
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        logger.info(
            "AIService initialized with model=%s, temperature=%.2f",
            self.model,
            self.temperature,
        )
    
    async def analyze_resume(
        self,
        resume_input: ResumeInput,
        system_prompt: str,
    ) -> ResumeScore:
        logger.info("Starting resume analysis for job: %s", resume_input.job_title)
        
        formatted_prompt = self._format_prompt(system_prompt, resume_input)
        
        try:
            completion = await self.client.beta.chat.completions.parse(
                model=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                messages=[
                    {
                        "role": "system",
                        "content": formatted_prompt,
                    },
                    {
                        "role": "user",
                        "content": (
                            "Analyze this resume and provide a detailed score "
                            "following the rubric. Be thorough in your reasoning."
                        ),
                    },
                ],
                response_format=ResumeScore,
            )
            
            result = completion.choices[0].message.parsed
            
            if result is None:
                logger.error("Failed to parse structured response from OpenAI")
                raise AIServiceError("Failed to parse response from AI model")
            
            logger.info(
                "Resume analysis completed successfully. Score: %d/100",
                result.score,
            )
            
            return result
            
        except RateLimitError as e:
            logger.error("OpenAI rate limit exceeded: %s", str(e))
            raise AIServiceError(
                "API rate limit exceeded. Please try again later."
            ) from e
            
        except APIConnectionError as e:
            logger.error("Failed to connect to OpenAI API: %s", str(e))
            raise AIServiceError(
                "Failed to connect to OpenAI API. Check your internet connection."
            ) from e
            
        except APIError as e:
            logger.error("OpenAI API error: %s", str(e))
            raise AIServiceError(f"OpenAI API error: {str(e)}") from e
            
        except Exception as e:
            logger.exception("Unexpected error during resume analysis")
            raise AIServiceError(f"Unexpected error: {str(e)}") from e
    
    def _format_prompt(
        self,
        template: str,
        resume_input: ResumeInput,
    ) -> str:
        requirements_text = "\n".join(f"- {req}" for req in resume_input.requirements)
        
        return template.format(
            job=resume_input.job_title,
            requirements=requirements_text,
            curriculum=resume_input.resume_text,
        )
    
    async def health_check(self) -> bool:
        try:
            await self.client.models.list()
            logger.info("OpenAI API health check passed")
            return True
        except Exception as e:
            logger.warning("OpenAI API health check failed: %s", str(e))
            return False

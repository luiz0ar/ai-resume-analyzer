from typing import List

from pydantic import BaseModel, Field


class ResumeInput(BaseModel):
    
    job_title: str = Field(
        ...,
        description="The title of the job position being applied for",
        min_length=1,
        examples=["Senior Python Developer"],
    )
    job_description: str = Field(
        ...,
        description="Detailed description of the job role and responsibilities",
        min_length=10,
        examples=["We are looking for a Senior Python Developer to join our team..."],
    )
    requirements: List[str] = Field(
        ...,
        description="List of required skills, qualifications, and experience",
        min_length=1,
        examples=[["5+ years Python", "FastAPI experience", "AWS knowledge"]],
    )
    resume_text: str = Field(
        ...,
        description="The candidate's resume content as plain text",
        min_length=50,
    )


class ResumeScore(BaseModel):
    
    reasoning: str = Field(
        ...,
        description=(
            "Detailed step-by-step explanation of the scoring decision. "
            "Include analysis of hard skills, experience, soft skills, and education. "
            "Explain how each rubric category contributed to the final score."
        ),
    )
    score: int = Field(
        ...,
        ge=0,
        le=100,
        description=(
            "Overall candidate score from 0 to 100 based on the scoring rubric. "
            "40 points max for hard skills, 25 for experience, 20 for soft skills, "
            "and 15 for education."
        ),
    )
    positive_points: List[str] = Field(
        ...,
        min_length=1,
        max_length=5,
        description=(
            "Top 3 strengths of the candidate. "
            "Focus on specific skills, achievements, or qualifications that match the job."
        ),
    )
    negative_points: List[str] = Field(
        ...,
        min_length=1,
        max_length=5,
        description=(
            "Top 3 gaps or areas of concern. "
            "Identify missing skills, lack of experience, or misalignments with requirements."
        ),
    )
    
    def to_summary(self) -> str:
        positives = "\n".join(f"{point}" for point in self.positive_points)
        negatives = "\n".join(f"{point}" for point in self.negative_points)
        
        return (
            f"\n{'='*60}\n"
            f"RESUME ANALYSIS RESULT\n"
            f"{'='*60}\n\n"
            f"SCORE: {self.score}/100\n\n"
            f"REASONING:\n{self.reasoning}\n\n"
            f"STRENGTHS:\n{positives}\n\n"
            f"GAPS:\n{negatives}\n"
            f"{'='*60}"
        )

from pydantic import BaseModel
from typing import List


class VacancyAnalysis(BaseModel):
    matching_skills: List[str]
    unconfirmed_skills: List[str]
    experience_match: bool
    recommendations: List[str]
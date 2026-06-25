from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, ConfigDict


# ----------------------------
# Candidate Creation Schema
# ----------------------------

class CandidateCreate(BaseModel):

    full_name: str

    email: Optional[EmailStr] = None

    phone: Optional[str] = None

    current_location: Optional[str] = None

    current_role: Optional[str] = None

    total_experience: Optional[float] = None

    professional_summary: Optional[str] = None

    primary_domain: Optional[str] = None

    education: Optional[list] = None

    skills: Optional[List[str]] = None

    projects: Optional[list] = None

    certifications: Optional[list] = None

    resume_file_name: Optional[str] = None

    resume_path: Optional[str] = None


# ----------------------------
# Candidate Response Schema
# ----------------------------

class CandidateResponse(CandidateCreate):

    id: str

    is_active: bool

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
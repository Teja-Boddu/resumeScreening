from uuid import uuid4
from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Float,
    DateTime,
    Boolean,
    JSON
)

from app.database.base import Base


class Candidate(Base):
    """
    Represents a candidate profile extracted from a resume.
    """

    __tablename__ = "candidates"

    # -----------------------------
    # Primary Key
    # -----------------------------
    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid4())
    )

    # -----------------------------
    # Basic Information
    # -----------------------------
    full_name = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        nullable=True
    )

    phone = Column(
        String,
        nullable=True
    )

    current_location = Column(
        String,
        nullable=True
    )

    # -----------------------------
    # Professional Information
    # -----------------------------
    current_role = Column(
        String,
        nullable=True
    )

    total_experience = Column(
        Float,
        nullable=True
    )

    professional_summary = Column(
        String,
        nullable=True
    )

    primary_domain = Column(
        String,
        nullable=True
    )

    # -----------------------------
    # AI Extracted Information
    # -----------------------------
    education = Column(
        JSON,
        nullable=True
    )

    skills = Column(
        JSON,
        nullable=True
    )

    projects = Column(
        JSON,
        nullable=True
    )

    certifications = Column(
        JSON,
        nullable=True
    )

    # -----------------------------
    # Resume Information
    # -----------------------------
    resume_file_name = Column(
        String,
        nullable=True
    )

    resume_path = Column(
        String,
        nullable=True
    )

    # -----------------------------
    # System Information
    # -----------------------------
    is_active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
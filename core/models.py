"""Pydantic models for CV Maker data validation.

All data is stored in a single JSON file. These models provide validation
and type safety for the data structures.
"""
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class SkillCategory(str, Enum):
    """Categories for skills."""

    LANGUAGE = "Language"
    FRAMEWORK = "Framework"
    TOOL = "Tool"
    DATABASE = "Database"
    CLOUD = "Cloud"
    SOFT = "Soft"
    OTHER = "Other"


class SkillLevel(str, Enum):
    """Proficiency levels for skills."""

    JUNIOR = "Junior"
    MID = "Mid"
    SENIOR = "Senior"
    EXPERT = "Expert"


class Profile(BaseModel):
    """User profile information."""

    name: str = ""
    emails: list[str] = Field(default_factory=list)
    phones: list[str] = Field(default_factory=list)
    location: str = ""
    linkedin: str = ""
    github: str = ""
    portfolio: str = ""
    headline: str = ""
    summary: str = ""


class Skill(BaseModel):
    """A technical or soft skill."""

    id: str
    name: str
    category: SkillCategory = SkillCategory.OTHER
    level: SkillLevel = SkillLevel.MID
    years: int = 0


class ExperienceVersion(BaseModel):
    """A specific version of an experience entry.

    Multiple versions allow tailoring the same job experience
    for different target roles.
    """

    id: str
    title: str
    description: str = ""
    bullets: list[str] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)  # Skill IDs
    created_at: datetime = Field(default_factory=datetime.now)
    is_default: bool = False


class Experience(BaseModel):
    """A work experience entry with multiple versions."""

    id: str
    company: str
    location: str = ""
    company_url: str = ""
    start_date: str  # YYYY-MM format
    end_date: Optional[str] = None  # YYYY-MM format, None if current
    is_current: bool = False
    versions: list[ExperienceVersion] = Field(default_factory=list)


class JobDescription(BaseModel):
    """A job description to tailor resumes for."""

    id: str
    title: str
    company: str
    text: str
    url: str = ""
    created_at: datetime = Field(default_factory=datetime.now)


class Resume(BaseModel):
    """A tailored resume assembled from experiences and skills."""

    id: str
    name: str
    jd_id: Optional[str] = None  # JobDescription ID
    selected_versions: list[str] = Field(default_factory=list)  # ExperienceVersion IDs
    selected_skills: list[str] = Field(default_factory=list)  # Skill IDs
    custom_summary: str = ""
    show_github: bool = True
    show_linkedin: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class ResumeBank(BaseModel):
    """Root model containing all CV Maker data."""

    profile: Profile = Field(default_factory=Profile)
    skills: list[Skill] = Field(default_factory=list)
    experiences: list[Experience] = Field(default_factory=list)
    job_descriptions: list[JobDescription] = Field(default_factory=list)
    resumes: list[Resume] = Field(default_factory=list)

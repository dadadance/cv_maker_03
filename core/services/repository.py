"""JSON Repository Service - Single source of truth for all data operations.

This module provides pure functions for loading, saving, and manipulating
the resume bank data stored in a JSON file.
"""
import json
from datetime import datetime
from functools import reduce
from pathlib import Path
from typing import Callable, Optional, TypeVar

from core.models import (
    Experience,
    ExperienceVersion,
    JobDescription,
    Profile,
    Resume,
    ResumeBank,
    Skill,
    SkillCategory,
    SkillLevel,
)

T = TypeVar("T")

# Default path - can be overridden
DEFAULT_DATA_PATH = Path(__file__).parent.parent.parent / "resume_bank" / "data.json"


# --- Pure Helper Functions ---


def pipe(value: T, *functions: Callable) -> T:
    """Pass value through a sequence of functions."""
    return reduce(lambda v, f: f(v), functions, value)


def generate_id(prefix: str, existing_ids: list[str]) -> str:
    """Generate a unique ID with the given prefix.

    Args:
        prefix: ID prefix (e.g., 'skill', 'exp', 'jd')
        existing_ids: List of existing IDs to avoid collision

    Returns:
        New unique ID like 'skill_001', 'exp_002', etc.
    """
    max_num = 0
    for id_ in existing_ids:
        if id_.startswith(f"{prefix}_"):
            try:
                num = int(id_.split("_")[1])
                max_num = max(max_num, num)
            except (IndexError, ValueError):
                continue
    return f"{prefix}_{max_num + 1:03d}"


def now_iso() -> str:
    """Return current datetime in ISO format."""
    return datetime.now().isoformat()


# --- File Operations ---


def load_data(path: Path = DEFAULT_DATA_PATH) -> ResumeBank:
    """Load and validate data from JSON file.

    Args:
        path: Path to JSON file

    Returns:
        Validated ResumeBank model

    Raises:
        FileNotFoundError: If file doesn't exist
        ValidationError: If data doesn't match schema
    """
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")

    with open(path, encoding="utf-8") as f:
        raw_data = json.load(f)

    return ResumeBank.model_validate(raw_data)


def save_data(data: ResumeBank, path: Path = DEFAULT_DATA_PATH) -> None:
    """Save data to JSON file with pretty formatting.

    Args:
        data: ResumeBank model to save
        path: Path to JSON file
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            data.model_dump(mode="json"),
            f,
            indent=2,
            ensure_ascii=False,
            default=str,
        )


def load_or_create(path: Path = DEFAULT_DATA_PATH) -> ResumeBank:
    """Load data from file or create empty ResumeBank if not exists."""
    try:
        return load_data(path)
    except FileNotFoundError:
        return ResumeBank()


# --- Profile Operations ---


def update_profile(data: ResumeBank, profile: Profile) -> ResumeBank:
    """Update profile in ResumeBank. Returns new ResumeBank."""
    return data.model_copy(update={"profile": profile})


def set_profile_field(data: ResumeBank, field: str, value: str | list[str]) -> ResumeBank:
    """Set a single profile field. Returns new ResumeBank."""
    profile_dict = data.profile.model_dump()
    profile_dict[field] = value
    new_profile = Profile.model_validate(profile_dict)
    return update_profile(data, new_profile)


# --- Skill Operations ---


def get_skill_ids(data: ResumeBank) -> list[str]:
    """Get all skill IDs."""
    return [s.id for s in data.skills]


def find_skill_by_id(data: ResumeBank, skill_id: str) -> Optional[Skill]:
    """Find skill by ID. Returns None if not found."""
    for skill in data.skills:
        if skill.id == skill_id:
            return skill
    return None


def find_skill_by_name(data: ResumeBank, name: str) -> Optional[Skill]:
    """Find skill by name (case-insensitive). Returns None if not found."""
    name_lower = name.lower()
    for skill in data.skills:
        if skill.name.lower() == name_lower:
            return skill
    return None


def add_skill(
    data: ResumeBank,
    name: str,
    category: SkillCategory = SkillCategory.OTHER,
    level: SkillLevel = SkillLevel.MID,
    years: int = 0,
) -> tuple[ResumeBank, Skill]:
    """Add a new skill. Returns tuple of (new ResumeBank, created Skill)."""
    skill_id = generate_id("skill", get_skill_ids(data))
    skill = Skill(id=skill_id, name=name, category=category, level=level, years=years)
    new_skills = data.skills + [skill]
    return data.model_copy(update={"skills": new_skills}), skill


def update_skill(data: ResumeBank, skill_id: str, **kwargs) -> ResumeBank:
    """Update an existing skill. Returns new ResumeBank."""
    new_skills = []
    for skill in data.skills:
        if skill.id == skill_id:
            skill_dict = skill.model_dump()
            skill_dict.update(kwargs)
            new_skills.append(Skill.model_validate(skill_dict))
        else:
            new_skills.append(skill)
    return data.model_copy(update={"skills": new_skills})


def delete_skill(data: ResumeBank, skill_id: str) -> ResumeBank:
    """Delete a skill by ID. Returns new ResumeBank."""
    new_skills = [s for s in data.skills if s.id != skill_id]
    return data.model_copy(update={"skills": new_skills})


# --- Experience Operations ---


def get_experience_ids(data: ResumeBank) -> list[str]:
    """Get all experience IDs."""
    return [e.id for e in data.experiences]


def get_all_version_ids(data: ResumeBank) -> list[str]:
    """Get all experience version IDs across all experiences."""
    ids = []
    for exp in data.experiences:
        for v in exp.versions:
            ids.append(v.id)
    return ids


def find_experience_by_id(data: ResumeBank, exp_id: str) -> Optional[Experience]:
    """Find experience by ID. Returns None if not found."""
    for exp in data.experiences:
        if exp.id == exp_id:
            return exp
    return None


def find_version_by_id(data: ResumeBank, version_id: str) -> Optional[tuple[Experience, ExperienceVersion]]:
    """Find experience version by ID. Returns tuple of (Experience, Version) or None."""
    for exp in data.experiences:
        for v in exp.versions:
            if v.id == version_id:
                return (exp, v)
    return None


def add_experience(
    data: ResumeBank,
    company: str,
    start_date: str,
    end_date: Optional[str] = None,
    is_current: bool = False,
    location: str = "",
    company_url: str = "",
) -> tuple[ResumeBank, Experience]:
    """Add a new experience (without versions). Returns tuple of (new ResumeBank, created Experience)."""
    exp_id = generate_id("exp", get_experience_ids(data))
    exp = Experience(
        id=exp_id,
        company=company,
        location=location,
        company_url=company_url,
        start_date=start_date,
        end_date=end_date,
        is_current=is_current,
        versions=[],
    )
    new_experiences = data.experiences + [exp]
    return data.model_copy(update={"experiences": new_experiences}), exp


def add_version(
    data: ResumeBank,
    exp_id: str,
    title: str,
    description: str = "",
    bullets: Optional[list[str]] = None,
    skills: Optional[list[str]] = None,
    is_default: bool = False,
) -> tuple[ResumeBank, ExperienceVersion]:
    """Add a new version to an experience. Returns tuple of (new ResumeBank, created Version)."""
    exp = find_experience_by_id(data, exp_id)
    if not exp:
        raise ValueError(f"Experience not found: {exp_id}")

    # Generate version ID
    version_num = len(exp.versions) + 1
    version_id = f"{exp_id}_v{version_num}"

    version = ExperienceVersion(
        id=version_id,
        title=title,
        description=description,
        bullets=bullets or [],
        skills=skills or [],
        created_at=datetime.now(),
        is_default=is_default,
    )

    # If this is the first version or marked as default, ensure only this one is default
    new_versions = []
    for v in exp.versions:
        if is_default:
            new_versions.append(v.model_copy(update={"is_default": False}))
        else:
            new_versions.append(v)
    new_versions.append(version)

    # If no default set and this is the first version, make it default
    if not any(v.is_default for v in new_versions):
        new_versions[-1] = new_versions[-1].model_copy(update={"is_default": True})

    new_exp = exp.model_copy(update={"versions": new_versions})

    new_experiences = [new_exp if e.id == exp_id else e for e in data.experiences]
    return data.model_copy(update={"experiences": new_experiences}), version


def update_experience(data: ResumeBank, exp_id: str, **kwargs) -> ResumeBank:
    """Update an experience (not versions). Returns new ResumeBank."""
    new_experiences = []
    for exp in data.experiences:
        if exp.id == exp_id:
            exp_dict = exp.model_dump()
            exp_dict.update(kwargs)
            new_experiences.append(Experience.model_validate(exp_dict))
        else:
            new_experiences.append(exp)
    return data.model_copy(update={"experiences": new_experiences})


def update_version(data: ResumeBank, version_id: str, **kwargs) -> ResumeBank:
    """Update an experience version. Returns new ResumeBank."""
    new_experiences = []
    for exp in data.experiences:
        new_versions = []
        for v in exp.versions:
            if v.id == version_id:
                v_dict = v.model_dump()
                v_dict.update(kwargs)
                new_versions.append(ExperienceVersion.model_validate(v_dict))
            else:
                new_versions.append(v)
        new_experiences.append(exp.model_copy(update={"versions": new_versions}))
    return data.model_copy(update={"experiences": new_experiences})


def delete_experience(data: ResumeBank, exp_id: str) -> ResumeBank:
    """Delete an experience and all its versions. Returns new ResumeBank."""
    new_experiences = [e for e in data.experiences if e.id != exp_id]
    return data.model_copy(update={"experiences": new_experiences})


def delete_version(data: ResumeBank, version_id: str) -> ResumeBank:
    """Delete an experience version. Returns new ResumeBank."""
    new_experiences = []
    for exp in data.experiences:
        new_versions = [v for v in exp.versions if v.id != version_id]
        new_experiences.append(exp.model_copy(update={"versions": new_versions}))
    return data.model_copy(update={"experiences": new_experiences})


# --- Job Description Operations ---


def get_jd_ids(data: ResumeBank) -> list[str]:
    """Get all job description IDs."""
    return [jd.id for jd in data.job_descriptions]


def find_jd_by_id(data: ResumeBank, jd_id: str) -> Optional[JobDescription]:
    """Find job description by ID. Returns None if not found."""
    for jd in data.job_descriptions:
        if jd.id == jd_id:
            return jd
    return None


def add_jd(
    data: ResumeBank,
    title: str,
    company: str,
    text: str,
    url: str = "",
) -> tuple[ResumeBank, JobDescription]:
    """Add a new job description. Returns tuple of (new ResumeBank, created JD)."""
    jd_id = generate_id("jd", get_jd_ids(data))
    jd = JobDescription(
        id=jd_id,
        title=title,
        company=company,
        text=text,
        url=url,
        created_at=datetime.now(),
    )
    new_jds = data.job_descriptions + [jd]
    return data.model_copy(update={"job_descriptions": new_jds}), jd


def update_jd(data: ResumeBank, jd_id: str, **kwargs) -> ResumeBank:
    """Update a job description. Returns new ResumeBank."""
    new_jds = []
    for jd in data.job_descriptions:
        if jd.id == jd_id:
            jd_dict = jd.model_dump()
            jd_dict.update(kwargs)
            new_jds.append(JobDescription.model_validate(jd_dict))
        else:
            new_jds.append(jd)
    return data.model_copy(update={"job_descriptions": new_jds})


def delete_jd(data: ResumeBank, jd_id: str) -> ResumeBank:
    """Delete a job description. Returns new ResumeBank."""
    new_jds = [jd for jd in data.job_descriptions if jd.id != jd_id]
    return data.model_copy(update={"job_descriptions": new_jds})


# --- Resume Operations ---


def get_resume_ids(data: ResumeBank) -> list[str]:
    """Get all resume IDs."""
    return [r.id for r in data.resumes]


def find_resume_by_id(data: ResumeBank, resume_id: str) -> Optional[Resume]:
    """Find resume by ID. Returns None if not found."""
    for resume in data.resumes:
        if resume.id == resume_id:
            return resume
    return None


def add_resume(
    data: ResumeBank,
    name: str,
    jd_id: Optional[str] = None,
    selected_versions: Optional[list[str]] = None,
    selected_skills: Optional[list[str]] = None,
    custom_summary: str = "",
) -> tuple[ResumeBank, Resume]:
    """Add a new resume. Returns tuple of (new ResumeBank, created Resume)."""
    resume_id = generate_id("resume", get_resume_ids(data))
    now = datetime.now()
    resume = Resume(
        id=resume_id,
        name=name,
        jd_id=jd_id,
        selected_versions=selected_versions or [],
        selected_skills=selected_skills or [],
        custom_summary=custom_summary,
        created_at=now,
        updated_at=now,
    )
    new_resumes = data.resumes + [resume]
    return data.model_copy(update={"resumes": new_resumes}), resume


def update_resume(data: ResumeBank, resume_id: str, **kwargs) -> ResumeBank:
    """Update a resume. Returns new ResumeBank."""
    kwargs["updated_at"] = datetime.now()
    new_resumes = []
    for resume in data.resumes:
        if resume.id == resume_id:
            r_dict = resume.model_dump()
            r_dict.update(kwargs)
            new_resumes.append(Resume.model_validate(r_dict))
        else:
            new_resumes.append(resume)
    return data.model_copy(update={"resumes": new_resumes})


def delete_resume(data: ResumeBank, resume_id: str) -> ResumeBank:
    """Delete a resume. Returns new ResumeBank."""
    new_resumes = [r for r in data.resumes if r.id != resume_id]
    return data.model_copy(update={"resumes": new_resumes})


# --- Convenience Functions ---


def with_save(func: Callable, path: Path = DEFAULT_DATA_PATH):
    """Decorator/wrapper to auto-save after mutation operations."""

    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, tuple) and isinstance(result[0], ResumeBank):
            save_data(result[0], path)
        elif isinstance(result, ResumeBank):
            save_data(result, path)
        return result

    return wrapper

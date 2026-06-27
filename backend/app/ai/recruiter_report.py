import json
import re
import requests

from app.ai.skill_extractor import SkillExtractor

OLLAMA_URL = "http://localhost:11434/api/generate"


class RecruiterReport:

    MODEL = "qwen2.5:3b"

    @classmethod
    def generate_report(

        cls,

        job_description: str,

        candidate

    ):

        required_skills = SkillExtractor.extract(
            job_description
        )

        prompt = f"""
You are an experienced Technical Recruiter.

Your task is to evaluate ONE candidate.

Return ONLY VALID JSON.

DO NOT explain.

DO NOT use markdown.

DO NOT write anything outside JSON.

Recommendation MUST be ONLY ONE of:

- Highly Recommended
- Recommended
- Consider
- Not Recommended

Strengths MUST contain ONLY matched technical skills.

Missing Skills MUST contain ONLY required skills missing from candidate.

Summary must be maximum 40 words.

Job Description

{job_description}

Required Skills

{", ".join(required_skills)}

Candidate

Name:
{candidate.full_name}

Role:
{candidate.current_role}

Experience:
{candidate.total_experience}

Education:
{candidate.education}

Skills:
{candidate.skills}

Projects:
{candidate.projects}

Certifications:
{candidate.certifications}

Return EXACTLY this JSON:

{{
"recommendation":"",
"strengths":[],
"missing_skills":[],
"summary":""
}}

"""

        response = requests.post(

            OLLAMA_URL,

            json={

                "model": cls.MODEL,

                "prompt": prompt,

                "stream": False,

                "think": False

            },

            timeout=180

        )

        response.raise_for_status()

        text = response.json()["response"]

        text = re.sub(

            r"```json|```",

            "",

            text

        ).strip()

        try:

            report = json.loads(text)

        except:

            report = {}

        return {

            "recommendation":

                report.get(

                    "recommendation",

                    "Consider"

                ),

            "strengths":

                report.get(

                    "strengths",

                    []

                ),

            "missing_skills":

                report.get(

                    "missing_skills",

                    []

                ),

            "summary":

                report.get(

                    "summary",

                    ""

                )

        }
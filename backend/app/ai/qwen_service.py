import json
import re
import requests


OLLAMA_URL = "http://localhost:11434/api/generate"


class QwenService:

    @staticmethod
    def extract_candidate_information(resume_text: str):

        prompt = f"""
You are an expert AI Resume Parser.

Extract the resume information.

Rules:

1. Return ONLY JSON.
2. No explanation.
3. No markdown.
4. Missing values should be null.
5. Skills must be a list.
6. Education must be a list.
7. Projects must be a list.
8. Certifications must be a list.

Return this JSON format exactly:

{{
    "full_name": "",
    "email": "",
    "phone": "",
    "current_location": "",
    "current_role": "",
    "total_experience": 0,
    "professional_summary": "",
    "primary_domain": "",
    "education": [],
    "skills": [],
    "projects": [],
    "certifications": [],
    "resume_file_name": "",
    "resume_path": ""
}}

Resume:

{resume_text}
"""

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "qwen3:8b",
                "prompt": prompt,
                "stream": False
            }
        )

        response.raise_for_status()

        result = response.json()["response"]

        # Remove markdown if present
        result = re.sub(r"```json|```", "", result).strip()

        return json.loads(result)
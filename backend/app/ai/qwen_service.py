import json
import re
import requests


OLLAMA_URL = "http://localhost:11434/api/generate"


class QwenService:

    MODEL_NAME = "qwen2.5:3b"

    @staticmethod
    def warmup():
        """
        Load the model into memory before processing resumes.
        """
        try:
            requests.post(
                OLLAMA_URL,
                json={
                    "model": QwenService.MODEL_NAME,
                    "prompt": "Hello",
                    "stream": False,
                    "think": False
                },
                timeout=60
            )
            print("✅ Qwen Warmup Completed")

        except Exception as e:
            print("⚠ Warmup Failed:", e)

    @staticmethod
    def extract_candidate_information(resume_text: str):

        # Limit resume size for faster inference
        resume_text = resume_text[:4000]

        prompt = f"""
Extract the following information from the resume.

Return ONLY valid JSON.

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
                "model": QwenService.MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "think": False
            },
            timeout=120
        )

        response.raise_for_status()

        result = response.json()["response"]

        # Remove markdown if present
        result = re.sub(r"```json|```", "", result).strip()

        try:
            return json.loads(result)

        except json.JSONDecodeError:

            print("\n========== INVALID QWEN RESPONSE ==========")
            print(result)
            print("===========================================\n")

            raise Exception(
                "Qwen returned invalid JSON."
            )
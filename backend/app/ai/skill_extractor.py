import re


class SkillExtractor:

    # Expand this list over time
    KNOWN_SKILLS = {

        "python",
        "java",
        "javascript",
        "typescript",
        "react",
        "angular",
        "vue",
        "node",
        "node.js",
        "express",
        "fastapi",
        "flask",
        "django",

        "docker",
        "kubernetes",
        "jenkins",
        "terraform",
        "ansible",

        "aws",
        "azure",
        "gcp",

        "postgresql",
        "mysql",
        "mongodb",
        "redis",
        "sqlite",

        "tensorflow",
        "pytorch",
        "transformers",
        "huggingface",

        "machine learning",
        "deep learning",

        "pandas",
        "numpy",

        "git",
        "github",

        "linux",

        "rest",
        "rest api",
        "rest apis",

        "microservices",

        "selenium",
        "testng",

        "spring",
        "spring boot",

        "network security",
        "siem"

    }

    @classmethod
    def extract_skills(
        cls,
        text: str
    ):

        text = text.lower()

        found = []

        for skill in cls.KNOWN_SKILLS:

            if skill in text:

                found.append(skill)

        return sorted(set(found))
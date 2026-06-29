import re


class SkillExtractor:

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
    def extract(cls, text: str):

        text = text.lower()

        found = []

        for skill in cls.KNOWN_SKILLS:

            pattern = r"\b" + re.escape(skill) + r"\b"

            if re.search(pattern, text):

                found.append(skill)

        return sorted(set(found))

    @classmethod
    def extract_skills(cls, text: str):
        """
        Backward compatibility.
        Existing code using extract_skills() will continue to work.
        """
        return cls.extract(text)
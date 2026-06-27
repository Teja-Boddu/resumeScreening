class SkillAlias:

    SKILL_MAP = {

        # Languages
        "python": "python",
        "java": "java",
        "javascript": "javascript",
        "js": "javascript",
        "typescript": "typescript",
        "ts": "typescript",

        # Backend
        "fastapi": "fastapi",
        "django": "django",
        "flask": "flask",
        "spring": "spring boot",
        "springboot": "spring boot",
        "spring boot": "spring boot",

        # Database
        "postgres": "postgresql",
        "postgresql": "postgresql",
        "mysql": "mysql",
        "mongodb": "mongodb",
        "mongo": "mongodb",

        # Cloud
        "aws": "aws",
        "azure": "azure",
        "gcp": "gcp",

        # DevOps
        "docker": "docker",
        "k8s": "kubernetes",
        "kubernetes": "kubernetes",
        "jenkins": "jenkins",

        # APIs
        "rest": "rest api",
        "rest api": "rest api",
        "rest apis": "rest api",
        "graphql": "graphql",

        # AI
        "ml": "machine learning",
        "machine learning": "machine learning",
        "deep learning": "deep learning",
        "dl": "deep learning",
        "llm": "large language models",

        # Version Control
        "git": "git",
        "github": "git"
    }

    @classmethod
    def normalize(cls, skill: str):

        skill = skill.lower().strip()

        return cls.SKILL_MAP.get(skill, skill)
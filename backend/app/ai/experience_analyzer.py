import re


class ExperienceAnalyzer:

    @staticmethod
    def extract_required_experience(job_description: str):

        text = job_description.lower()

        patterns = [

            r"(\d+)\+\s*years",

            r"(\d+)\s*years",

            r"minimum\s*(\d+)\s*years",

            r"at least\s*(\d+)\s*years",

            r"(\d+)\s*-\s*(\d+)\s*years"

        ]

        for pattern in patterns:

            match = re.search(pattern, text)

            if match:

                return int(match.group(1))

        return 0
import re


class RegexParser:

    @staticmethod
    def extract_email(text: str):

        match = re.search(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            text
        )

        if match:
            return match.group(0)

        return None


    @staticmethod
    def extract_phone(text: str):

        match = re.search(
            r"(?:\+91[\s-]?)?[6-9]\d{9}",
            text
        )

        if match:
            return match.group(0)

        return None

    @staticmethod
    def extract_name(text: str):

        lines = text.splitlines()

        for line in lines:

            line = line.strip()

            if line:

                return line

        return ""
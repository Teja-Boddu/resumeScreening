class EducationNormalizer:

    DEGREE_MAP = {

        # Bachelor's
        "b.tech": "bachelor",
        "btech": "bachelor",
        "be": "bachelor",
        "b.e": "bachelor",
        "bachelor": "bachelor",
        "bachelor of technology": "bachelor",
        "bachelor of engineering": "bachelor",
        "bachelor of science": "bachelor",
        "b.sc": "bachelor",

        # Master's
        "m.tech": "master",
        "mtech": "master",
        "me": "master",
        "m.e": "master",
        "master": "master",
        "master of technology": "master",
        "master of engineering": "master",
        "master of science": "master",
        "m.sc": "master",
        "ms": "master",

        # Doctorate
        "phd": "doctorate",
        "doctorate": "doctorate"
    }

    @classmethod
    def normalize(cls, text: str):

        text = text.lower()

        for key, value in cls.DEGREE_MAP.items():

            if key in text:

                return value

        return "unknown"
from app.ai.skill_alias import SkillAlias
from app.ai.skill_extractor import SkillExtractor
from app.ai.experience_analyzer import ExperienceAnalyzer
from app.ai.education_normalizer import EducationNormalizer


class ScoringService:

    @staticmethod
    def skill_score(
        job_description: str,
        candidate
    ):

        # Extract skills from Job Description
        jd_skills = SkillExtractor.extract(
            job_description
        )

        # Normalize JD skills
        jd_skills = {

            SkillAlias.normalize(skill)

            for skill in jd_skills

        }

        # Normalize Candidate skills
        candidate_skills = {

            SkillAlias.normalize(skill)

            for skill in (candidate.skills or [])

        }

        matched = jd_skills.intersection(
            candidate_skills
        )

        if len(jd_skills) == 0:
            return 0

        return round(

            (len(matched) / len(jd_skills)) * 100,

            2

        )

    @staticmethod
    def experience_score(
        job_description: str,
        candidate
    ):

        required = ExperienceAnalyzer.extract_required_experience(
            job_description
        )

        if required is None:
            return 100

        actual = candidate.total_experience or 0

        if actual >= required:
            return 100

        percentage = (

            actual / required

        ) * 100

        return round(
            percentage,
            2
        )

    @staticmethod
    def education_score(
        job_description: str,
        candidate
    ):

        jd = job_description.lower()

        if "master" in jd:

            required = "master"

        elif (
            "bachelor" in jd
            or "b.tech" in jd
            or "be" in jd
        ):

            required = "bachelor"

        else:

            return 100

        education = candidate.education or []

        if len(education) == 0:

            return 30

        highest = "unknown"

        for edu in education:

            if isinstance(edu, dict):

                text = " ".join(

                    str(v)

                    for v in edu.values()

                )

            else:

                text = str(edu)

            level = EducationNormalizer.normalize(
                text
            )

            if level == "doctorate":

                highest = "doctorate"

                break

            elif level == "master":

                highest = "master"

            elif (

                level == "bachelor"

                and highest == "unknown"

            ):

                highest = "bachelor"

        order = {

            "unknown": 0,

            "bachelor": 1,

            "master": 2,

            "doctorate": 3

        }

        if order[highest] >= order[required]:

            return 100

        return round(

            (

                order[highest]

                / order[required]

            ) * 100,

            2

        )

    @staticmethod
    def final_score(

        semantic,

        skill,

        experience,

        education,

        reranker

    ):

        score = (

            semantic * 0.20

            +

            reranker * 0.40

            +

            skill * 0.20

            +

            experience * 0.10

            +

            education * 0.10

        )

        return round(
            score,
            2
        )
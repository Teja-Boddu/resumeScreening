class CandidateNormalizer:

    @staticmethod
    def normalize(candidate: dict) -> dict:

        # -----------------------------
        # Full Name
        # -----------------------------
        candidate["full_name"] = (
            candidate.get("full_name") or ""
        ).strip()

        # -----------------------------
        # Primary Domain
        # -----------------------------
        candidate["primary_domain"] = (
            candidate.get("primary_domain") or ""
        ).strip()

        # -----------------------------
        # Education
        # Always convert into:
        # [
        #   {
        #      degree:"",
        #      field_of_study:""
        #   }
        # ]
        # -----------------------------

        normalized_education = []

        for edu in candidate.get("education", []):

            if isinstance(edu, str):

                normalized_education.append({

                    "degree": edu,

                    "field_of_study": ""

                })

            elif isinstance(edu, dict):

                normalized_education.append({

                    "degree": edu.get(
                        "degree",
                        ""
                    ),

                    "field_of_study": edu.get(
                        "field_of_study",
                        edu.get(
                            "field",
                            ""
                        )
                    )

                })

        candidate["education"] = normalized_education

        # -----------------------------
        # Projects
        # Always convert into list[str]
        # -----------------------------

        normalized_projects = []

        for project in candidate.get("projects", []):

            if isinstance(project, str):

                normalized_projects.append(project)

            elif isinstance(project, dict):

                normalized_projects.append(

                    project.get(
                        "name",
                        ""
                    )

                )

        candidate["projects"] = normalized_projects

        # -----------------------------
        # Certifications
        # Always convert into list[str]
        # -----------------------------

        normalized_certifications = []

        for cert in candidate.get(
            "certifications",
            []
        ):

            if isinstance(cert, str):

                normalized_certifications.append(cert)

            elif isinstance(cert, dict):

                normalized_certifications.append(

                    cert.get(
                        "name",
                        ""
                    )

                )

        candidate["certifications"] = normalized_certifications

        # -----------------------------
        # Skills
        # -----------------------------

        candidate["skills"] = [

            skill.strip()

            for skill in candidate.get(
                "skills",
                []
            )

            if skill
        ]

        return candidate
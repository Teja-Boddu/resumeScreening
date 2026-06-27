from app.models.candidate import Candidate


class DocumentBuilder:

    @staticmethod
    def build_candidate_document(
        candidate: Candidate
    ) -> str:

        # -----------------------------
        # Education
        # -----------------------------

        education_list = []

        for edu in (candidate.education or []):

            if isinstance(edu, dict):

                education_list.append(

                    f"{edu.get('degree', '')} "
                    f"{edu.get('field', '')} "
                    f"{edu.get('institution', '')}"

                )

            else:

                education_list.append(str(edu))

        education = "\n".join(education_list)

        # -----------------------------
        # Projects
        # -----------------------------

        project_list = []

        for project in (candidate.projects or []):

            if isinstance(project, dict):

                project_list.append(

                    project.get("name", "")

                )

            else:

                project_list.append(str(project))

        projects = "\n".join(project_list)

        # -----------------------------
        # Certifications
        # -----------------------------

        certifications = "\n".join(

            str(cert)

            for cert in (candidate.certifications or [])

        )

        # -----------------------------
        # Skills
        # -----------------------------

        skills = ", ".join(

            str(skill)

            for skill in (candidate.skills or [])

        )

        # -----------------------------
        # Document
        # -----------------------------

        document = f"""
Candidate Name:
{candidate.full_name}

Current Role:
{candidate.current_role}

Experience:
{candidate.total_experience} Years

Current Location:
{candidate.current_location}

Primary Domain:
{candidate.primary_domain}

Professional Summary:
{candidate.professional_summary}

Skills:
{skills}

Education:
{education}

Projects:
{projects}

Certifications:
{certifications}
"""

        return document.strip()
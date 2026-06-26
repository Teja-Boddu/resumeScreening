from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.utils.file_manager import (
    save_uploaded_zip,
    create_batch_folder,
    extract_zip,
    delete_temp_file
)

from app.parsers.parser_factory import ParserFactory
from app.ai.qwen_service import QwenService

from app.schemas.candidate_schema import CandidateCreate
from app.services.candidate_service import CandidateService


class ResumeService:

    @staticmethod
    def upload_resume_batch(
        upload_file: UploadFile,
        db: Session
    ):

        # Step 1: Save uploaded ZIP
        zip_path = save_uploaded_zip(upload_file)

        # Step 2: Create unique batch folder
        batch_id, batch_path = create_batch_folder()

        # Step 3: Extract ZIP
        extracted_files = extract_zip(
            zip_path,
            batch_path
        )

        # Step 4: Delete uploaded ZIP
        delete_temp_file(zip_path)

        saved_candidates = []
        failed_candidates = []

        # Step 5: Process every resume

        for file in extracted_files:

            if not file.is_file():
                continue

            try:

                print(f"\nProcessing Resume: {file.name}")

                # Extract resume text
                resume_text = ParserFactory.extract_text(
                    str(file)
                )

                # AI Extraction
                candidate_json = QwenService.extract_candidate_information(
                    resume_text
                )

                candidate_json["resume_file_name"] = file.name
                candidate_json["resume_path"] = str(file)

                # Validate using Pydantic
                candidate_schema = CandidateCreate(
                    **candidate_json
                )

                # Save into PostgreSQL
                candidate = CandidateService.create_candidate(
                    db=db,
                    candidate_data=candidate_schema
                )

                saved_candidates.append({
                    "id": str(candidate.id),
                    "name": candidate.full_name
                })

                print("Saved Successfully")

            except Exception as e:

                print(e)

                failed_candidates.append({
                    "resume": file.name,
                    "reason": str(e)
                })

        return {

            "batch_id": batch_id,

            "processed": len(extracted_files),

            "saved": len(saved_candidates),

            "failed": len(failed_candidates),

            "saved_candidates": saved_candidates,

            "failed_candidates": failed_candidates

        }
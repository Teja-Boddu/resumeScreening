from fastapi import UploadFile

from app.utils.file_manager import (
    save_uploaded_zip,
    create_batch_folder,
    extract_zip,
    delete_temp_file
)

from app.parsers.parser_factory import ParserFactory
from app.ai.qwen_service import QwenService


class ResumeService:

    @staticmethod
    def upload_resume_batch(upload_file: UploadFile):

        # Save uploaded ZIP
        zip_path = save_uploaded_zip(upload_file)

        # Create unique batch folder
        batch_id, batch_path = create_batch_folder()

        # Extract ZIP
        extracted_files = extract_zip(zip_path, batch_path)

        # Delete uploaded ZIP
        delete_temp_file(zip_path)

        parsed_candidates = []

        for file in extracted_files:

            if file.is_file():

                # Step 1: Extract text from resume
                resume_text = ParserFactory.extract_text(str(file))

                # Step 2: Send text to Qwen3
                candidate = QwenService.extract_candidate_information(
                    resume_text
                )

                # Step 3: Store file information
                candidate["resume_file_name"] = file.name
                candidate["resume_path"] = str(file)

                parsed_candidates.append(candidate)

        return {
            "batch_id": batch_id,
            "total_files": len(parsed_candidates),
            "candidates": parsed_candidates
        }
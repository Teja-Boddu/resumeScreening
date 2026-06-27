from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.utils.file_manager import (
    save_uploaded_zip,
    create_batch_folder,
    extract_zip,
    delete_temp_file
)

from app.parsers.parser_factory import ParserFactory
from app.parsers.regex_parser import RegexParser

from app.ai.qwen_service import QwenService
from app.ai.embedding_service import EmbeddingService
from app.ai.qdrant_service import QdrantService

from app.schemas.candidate_schema import CandidateCreate
from app.services.candidate_service import CandidateService

from app.ai.document_builder import DocumentBuilder

import time
from app.ai.document_builder import DocumentBuilder
from app.ai.candidate_normalizer import CandidateNormalizer


class ResumeService:

    @staticmethod
    def upload_resume_batch(
        upload_file: UploadFile,
        db: Session
    ):

        zip_path = save_uploaded_zip(upload_file)

        batch_id, batch_path = create_batch_folder()

        extracted_files = extract_zip(
            zip_path,
            batch_path
        )

        delete_temp_file(zip_path)

        saved_candidates = []
        failed_candidates = []

        # Warm up Qwen once
        # Warm up Qwen once
        if not getattr(QwenService, "_is_warm", False):
            QwenService.warmup()
            QwenService._is_warm = True

        for file in extracted_files:

            if not file.is_file():
                continue

            try:

                print("\n====================================")
                print(f"Processing Resume : {file.name}")
                print("====================================")

                # -----------------------------
                # Resume Text Extraction
                # -----------------------------

                start = time.time()

                resume_text = ParserFactory.extract_text(
                    str(file)
                )

                print("\n========== RESUME TEXT ==========")
                print(resume_text)
                print("=================================\n")

                regex_email = RegexParser.extract_email(
                    resume_text
                )

                regex_phone = RegexParser.extract_phone(
                    resume_text
                )

                regex_name = RegexParser.extract_name(
                    resume_text
                )

                print("Regex Email :", regex_email)
                print("Regex Phone :", regex_phone)

                print(
                    f"Resume Text Extraction : {time.time() - start:.2f} sec"
                )

                # -----------------------------
                # Qwen Extraction
                # -----------------------------

                start = time.time()

                # candidate_json = QwenService.extract_candidate_information(
                #     resume_text
                # )
                candidate_json = QwenService.extract_candidate_information(
                    resume_text
                )

                candidate_json = CandidateNormalizer.normalize(
                    candidate_json
                )

                print("\n========== QWEN OUTPUT ==========")
                print(candidate_json)
                print("=================================\n")

                # Override Email & Phone using Regex

                if regex_email:
                    candidate_json["email"] = regex_email

                if regex_phone:
                    candidate_json["phone"] = regex_phone

                if not candidate_json.get("full_name"):

                    candidate_json["full_name"] = regex_name

                print("\n========== FINAL JSON ==========")
                print(candidate_json)
                print("=================================\n")

                print(
                    f"Qwen Extraction : {time.time() - start:.2f} sec"
                )

                candidate_json["resume_file_name"] = file.name
                candidate_json["resume_path"] = str(file)

                candidate_schema = CandidateCreate(
                    **candidate_json
                )

                # -----------------------------
                # PostgreSQL
                # -----------------------------

                start = time.time()

                existing_candidate = CandidateService.get_candidate_by_email(
                    db=db,
                    email=candidate_schema.email
                )

                if existing_candidate:

                    candidate = CandidateService.update_candidate(
                        db=db,
                        candidate=existing_candidate,
                        candidate_data=candidate_schema
                    )

                    print("✅ Candidate Updated")

                else:

                    candidate = CandidateService.create_candidate(
                        db=db,
                        candidate_data=candidate_schema
                    )

                    print("✅ Candidate Created")

                print(
                    f"PostgreSQL Save/Update : {time.time() - start:.2f} sec"
                )

                # -----------------------------
                # Embedding Text
                # -----------------------------

                # text_for_embedding = f"""
                # Name: {candidate.full_name}
                # Role: {candidate.current_role}
                # Experience: {candidate.total_experience}
                # Skills: {", ".join(candidate.skills)}
                # Summary: {candidate.professional_summary}
                # """

                

                text_for_embedding = DocumentBuilder.build_candidate_document(
                    candidate
                )

                # -----------------------------
                # Embedding Generation
                # -----------------------------

                start = time.time()

                embedding = EmbeddingService.generate_embedding(
                    text_for_embedding
                )

                print(
                    f"Embedding Generation : {time.time() - start:.2f} sec"
                )

                # -----------------------------
                # Qdrant
                # -----------------------------

                start = time.time()

                QdrantService.store_candidate_embedding(
                candidate=candidate,
                embedding=embedding
                )

                print(
                    f"Qdrant Upload : {time.time() - start:.2f} sec"
                )

                saved_candidates.append({
                    "id": str(candidate.id),
                    "name": candidate.full_name
                })

                print("✅ Resume Processed Successfully")

            except Exception as e:

                print("\n❌ ERROR")
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
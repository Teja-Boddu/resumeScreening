from fastapi import APIRouter, UploadFile, File

from app.services.resume_service import ResumeService

router = APIRouter()


@router.post("/upload")
def upload_resume_zip(
    file: UploadFile = File(...)
):
    """
    Upload a ZIP file containing resumes.
    """

    return ResumeService.upload_resume_batch(file)
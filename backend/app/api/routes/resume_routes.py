from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from app.database.postgres import get_db
from app.services.resume_service import ResumeService

router = APIRouter()


@router.post("/upload")
def upload_resume_zip(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload a ZIP file containing resumes.
    """

    return ResumeService.upload_resume_batch(
        upload_file=file,
        db=db
    )
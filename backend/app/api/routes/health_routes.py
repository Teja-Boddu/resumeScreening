from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def health_check():

    return {
        "status": "Running",
        "message": "AI Resume Screening Backend is Healthy"
    }
from pydantic import BaseModel


class JobDescription(BaseModel):

    job_description: str

    top_k: int = 5
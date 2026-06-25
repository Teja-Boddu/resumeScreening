from pathlib import Path
from uuid import uuid4
import shutil
import zipfile

UPLOAD_DIR = Path("uploads")
TEMP_DIR = UPLOAD_DIR / "temp"
BATCH_DIR = UPLOAD_DIR / "batches"

TEMP_DIR.mkdir(parents=True, exist_ok=True)
BATCH_DIR.mkdir(parents=True, exist_ok=True)


def save_uploaded_zip(upload_file):

    file_path = TEMP_DIR / upload_file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    return file_path


def create_batch_folder():

    batch_id = str(uuid4())

    batch_path = BATCH_DIR / batch_id

    batch_path.mkdir(parents=True, exist_ok=True)

    return batch_id, batch_path


def extract_zip(zip_path, batch_path):

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(batch_path)

    return list(batch_path.iterdir())


def delete_temp_file(file_path):

    if file_path.exists():
        file_path.unlink()
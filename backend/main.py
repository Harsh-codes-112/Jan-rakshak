import hashlib
import os
import secrets
from functools import lru_cache

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from fastapi import BackgroundTasks, FastAPI, File, Form, HTTPException, UploadFile
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from models import Base, Complaint, Evidence

app = FastAPI(title="JAN-RAKSHAK API", version="1.0")
MAX_FILE_SIZE = 10 * 1024 * 1024
MAX_FILES = 5


@lru_cache(maxsize=1)
def get_engine():
    url = os.environ.get("DATABASE_URL", "").strip()
    if not url:
        raise RuntimeError("DATABASE_URL is not configured")
    if url.startswith("postgres://"):
        url = "postgresql+psycopg2://" + url.removeprefix("postgres://")
    elif url.startswith("postgresql://"):
        url = "postgresql+psycopg2://" + url.removeprefix("postgresql://")
    return create_engine(url, pool_pre_ping=True, pool_size=1, max_overflow=0)


def get_session_factory():
    return sessionmaker(bind=get_engine(), autoflush=False, expire_on_commit=False)


def get_object_store():
    bucket = os.environ.get("S3_BUCKET")
    if not bucket or not os.environ.get("AWS_ACCESS_KEY_ID") or not os.environ.get("AWS_SECRET_ACCESS_KEY"):
        raise HTTPException(
            status_code=503,
            detail="Evidence storage is not configured. Configure S3_BUCKET and AWS credentials before uploading files.",
        )
    options = {"region_name": os.environ.get("AWS_REGION", "us-east-1")}
    endpoint = os.environ.get("S3_ENDPOINT_URL")
    if endpoint:
        options["endpoint_url"] = endpoint
    return boto3.client("s3", **options), bucket


@app.get("/")
def root():
    return {"status": "ok", "service": "JAN-RAKSHAK API", "docs": "/docs"}


@app.get("/health")
def health_check():
    try:
        with get_engine().connect() as connection:
            connection.execute(text("SELECT 1"))
    except (RuntimeError, SQLAlchemyError):
        raise HTTPException(status_code=503, detail="Database is unavailable or not configured")
    return {"status": "healthy"}


def generate_file_hash(file_bytes: bytes) -> str:
    return hashlib.sha256(file_bytes).hexdigest()


def trigger_rag_legal_analysis(complaint_id: str, text_content: str):
    # Placeholder only: legal/RAG analysis is not implemented.
    return None


@app.post("/api/complaints/submit", status_code=201)
async def submit_complaint(
    background_tasks: BackgroundTasks,
    title: str = Form(..., min_length=1, max_length=200),
    description: str = Form(..., min_length=50),
    category: str = Form(..., min_length=1, max_length=100),
    is_anonymous: bool = Form(False),
    latitude: float | None = Form(None),
    longitude: float | None = Form(None),
    files: list[UploadFile] | None = File(None),
):
    if files and len(files) > MAX_FILES:
        raise HTTPException(status_code=400, detail=f"Upload no more than {MAX_FILES} files.")

    payloads = []
    for upload in files or []:
        content = await upload.read(MAX_FILE_SIZE + 1)
        await upload.close()
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="Each evidence file must be no larger than 10 MB.")
        payloads.append((upload, content, generate_file_hash(content)))

    s3 = None
    bucket = None
    if payloads:
        s3, bucket = get_object_store()

    tracking_id = "JR-" + secrets.token_hex(4).upper()
    stored_keys = []
    try:
        with get_session_factory()() as session:
            complaint = Complaint(
                tracking_id=tracking_id,
                title=title,
                description=description,
                category=category,
                is_anonymous=is_anonymous,
                latitude=latitude,
                longitude=longitude,
                status="SUBMITTED",
            )
            session.add(complaint)
            session.flush()

            for upload, content, digest in payloads:
                key = f"evidence/{tracking_id}/{secrets.token_hex(16)}"
                try:
                    s3.put_object(
                        Bucket=bucket,
                        Key=key,
                        Body=content,
                        ContentType=upload.content_type or "application/octet-stream",
                        ServerSideEncryption="AES256",
                    )
                except (BotoCoreError, ClientError) as exc:
                    raise HTTPException(status_code=502, detail="Could not store evidence file.") from exc
                stored_keys.append(key)
                session.add(
                    Evidence(
                        complaint_id=complaint.id,
                        file_path=f"s3://{bucket}/{key}",
                        file_type=upload.content_type or "application/octet-stream",
                        sha256_hash=digest,
                    )
                )
            session.commit()
    except HTTPException:
        if s3 and bucket:
            for key in stored_keys:
                try:
                    s3.delete_object(Bucket=bucket, Key=key)
                except (BotoCoreError, ClientError):
                    pass
        raise
    except (RuntimeError, SQLAlchemyError) as exc:
        if s3 and bucket:
            for key in stored_keys:
                try:
                    s3.delete_object(Bucket=bucket, Key=key)
                except (BotoCoreError, ClientError):
                    pass
        raise HTTPException(status_code=503, detail="Database is unavailable or could not save the complaint.") from exc

    # Do not use in-process background work for production jobs on serverless functions.
    # Return an honest status until a durable job queue and analysis service are configured.
    return {
        "status": "success",
        "tracking_id": tracking_id,
        "evidence_count": len(payloads),
        "message": "Complaint submitted. Automated legal analysis is not configured.",
    }

# main.py
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from pydantic import BaseModel
import hashlib

app = FastAPI(title="JAN-RAKSHAK API", version="1.0")


class ComplaintCreate(BaseModel):
    title: str
    description: str
    category: str
    is_anonymous: bool = False
    latitude: float | None = None
    longitude: float | None = None


@app.get("/")
async def root():
    return {"status": "ok", "service": "JAN-RAKSHAK API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


def generate_file_hash(file_bytes: bytes) -> str:
    return hashlib.sha256(file_bytes).hexdigest()


def trigger_rag_legal_analysis(complaint_id: str, text: str):
    """
    Simulated RAG workflow connecting to Vector DB containing BNS, BNSS, BSA.
    """
    # 1. Embed text using local/API NLP model.
    # 2. Query Pinecone/Qdrant for similar legal precedents and code sections.
    # 3. Generate summary via LLM.
    # 4. Save to AIAnalysis table.
    pass


@app.post("/api/complaints/submit")
async def submit_complaint(
    complaint: ComplaintCreate,
    background_tasks: BackgroundTasks,
    files: list[UploadFile] | None = File(default=None),
):
    if len(complaint.description) < 50:
        raise HTTPException(status_code=400, detail="Description too brief.")

    tracking_id = "JR-" + hashlib.md5(complaint.title.encode()).hexdigest()[:8].upper()

    evidence_records = []
    if files is not None:
        for file in files:
            content = await file.read()
            file_hash = generate_file_hash(content)
            evidence_records.append({"filename": file.filename, "hash": file_hash})

    background_tasks.add_task(trigger_rag_legal_analysis, tracking_id, complaint.description)

    return {
        "status": "success",
        "tracking_id": tracking_id,
        "evidence_secured": len(evidence_records),
        "message": "Complaint submitted successfully. AI legal analysis is underway.",
    }

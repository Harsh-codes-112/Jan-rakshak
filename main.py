from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from pydantic import BaseModel
import hashlib
from typing import List

app = FastAPI(title="JAN-RAKSHAK API", version="1.0")

class ComplaintCreate(BaseModel):
    title: str
    description: str
    category: str
    is_anonymous: bool
    latitude: float = None
    longitude: float = None

def generate_file_hash(file_bytes: bytes) -> str:
    return hashlib.sha256(file_bytes).hexdigest()

def trigger_rag_legal_analysis(tracking_id: str, text: str):
    # Simulated RAG background workflow
    pass

@app.post("/api/complaints/submit")
async def submit_complaint(
    complaint: ComplaintCreate, 
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...)
):
    if len(complaint.description) < 50:
        raise HTTPException(status_code=400, detail="Description too brief.")
    
    tracking_id = "JR-" + hashlib.md5(complaint.title.encode()).hexdigest()[:8].upper()
    
    evidence_records = []
    for file in files:
        content = await file.read()
        file_hash = generate_file_hash(content)
        evidence_records.append({"filename": file.filename, "hash": file_hash})

    background_tasks.add_task(trigger_rag_legal_analysis, tracking_id, complaint.description)
    
    return {
        "status": "success",
        "tracking_id": tracking_id,
        "evidence_secured": len(evidence_records),
        "message": "Complaint submitted successfully. AI analysis started."
    }

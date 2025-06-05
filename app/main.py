from fastapi import FastAPI
from app.models import IngestRequest, StatusResponse
from app.processor import enqueue_request, get_status
import uuid

app = FastAPI()

@app.post("/ingest")
def ingest(data: IngestRequest):
    ingestion_id = str(uuid.uuid4())
    enqueue_request(ingestion_id, data)
    return {"ingestion_id": ingestion_id}

@app.get("/status/{ingestion_id}", response_model=StatusResponse)
def status(ingestion_id: str):
    return get_status(ingestion_id)

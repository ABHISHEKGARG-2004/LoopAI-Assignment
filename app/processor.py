import asyncio
import uuid
import threading
from app.storage import queue, requests, batches, lock
from app.models import IngestRequest, Batch

def enqueue_request(ingestion_id, ingest_data: IngestRequest):
    with lock:
        ids = ingest_data.ids
        request_batches = []
        for i in range(0, len(ids), 3):
            batch_ids = ids[i:i+3]
            batch_id = str(uuid.uuid4())
            request_batches.append(Batch(batch_id=batch_id, ids=batch_ids, status="yet_to_start"))
        requests[ingestion_id] = request_batches
        queue[ingest_data.priority].append((ingestion_id, len(request_batches)))
        if ingestion_id not in batches:
            batches[ingestion_id] = request_batches

def get_status(ingestion_id):
    request_batches = batches.get(ingestion_id, [])
    if not request_batches:
        return {"ingestion_id": ingestion_id, "status": "yet_to_start", "batches": []}
    
    statuses = [b.status for b in request_batches]
    if all(s == "yet_to_start" for s in statuses):
        overall = "yet_to_start"
    elif all(s == "completed" for s in statuses):
        overall = "completed"
    else:
        overall = "triggered"
    
    return {
        "ingestion_id": ingestion_id,
        "status": overall,
        "batches": request_batches
    }

async def process_batch(batch: Batch):
    batch.status = "triggered"
    await asyncio.sleep(1)
    batch.status = "completed"

async def dispatcher():
    while True:
        found = False
        for priority in ["HIGH", "MEDIUM", "LOW"]:
            if queue[priority]:
                with lock:
                    ingestion_id, _ = queue[priority][0]
                    batch = next((b for b in batches[ingestion_id] if b.status == "yet_to_start"), None)
                    if batch:
                        found = True
                        asyncio.create_task(process_batch(batch))
                        break
                    else:
                        queue[priority].popleft()
        await asyncio.sleep(5 if found else 1)

def start_dispatcher():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(dispatcher())
    loop.run_forever()

threading.Thread(target=start_dispatcher, daemon=True).start()

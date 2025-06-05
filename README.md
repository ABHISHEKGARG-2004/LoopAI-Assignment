# 🚀 LoopAI Assignment – Data Ingestion API System

This project implements a RESTful API system to handle data ingestion requests asynchronously, with support for batching, rate limiting, and priority-based execution.

---

## 🌐 Live Deployment

**Base URL**:  
(https://loopai-assignment.onrender.com)

---

## 📌 Features

-  **POST /ingest** – Accepts IDs with priority and starts ingestion
-  **GET /status/{ingestion_id}** – Tracks status of ingestion request
-  **Priority-based Queuing** – Processes `HIGH` priority requests before `MEDIUM` and `LOW`
-  **Rate Limiting** – Processes only 1 batch every 5 seconds
-  **Batching** – Each batch contains **up to 3 IDs**
-  **Asynchronous Processing** using background tasks
-  In-memory persistence for ingestion and batch tracking

---

## 📦 Installation (Local Setup)

```bash
git clone https://github.com/ABHISHEKGARG-2004/LoopAI-Assignment.git
cd LoopAI-Assignment

# Create virtual environment
python -m venv venv
venv\Scripts\activate   # Use `source venv/bin/activate` for Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload

# backend/app/main.py

# IMPORTANT: Load environment variables at the very top
# This ensures they are available for all imported modules, like the triage_service
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import os

from .models import TriageRequest, TriageResponse
from .services.triage_service import triage_message # Now this import is safe

app = FastAPI(
    title="Customer Inquiry Triage API (Gemini Edition)",
    description="An API to automatically categorize customer support messages using Google Gemini.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    # This check remains a good safeguard.
    if not os.getenv("GOOGLE_API_KEY"):
        raise RuntimeError("FATAL: GOOGLE_API_KEY environment variable is not set. Please check your .env file.")
    print("Google API Key found. Triage service is ready.")

@app.get("/", summary="Root", include_in_schema=False)
async def read_root():
    return {"status": "ok", "message": "Gemini Triage API is running."}

@app.post("/triage",
            response_model=TriageResponse,
            summary="Triage a customer message",
            description="Accepts a customer message and returns its category, reasoning, and confidence score.",
            status_code=status.HTTP_200_OK)
async def triage_endpoint(request: TriageRequest):
    if not request.message or not request.message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty."
        )

    try:
        response_data = await triage_message(request.message)
        return response_data
    except Exception as e:
        print(f"An error occurred during triage: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing the message. Please check the backend logs."
        )
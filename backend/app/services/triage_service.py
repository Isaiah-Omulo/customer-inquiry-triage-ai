# backend/app/services/triage_service.py

import os
import google.generativeai as genai
import instructor
from typing import List

from ..models import TriageResponse, Category

# Configure the base Gemini client.
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Create an instructor-compatible client.
client = instructor.from_gemini(
    client=genai.GenerativeModel("gemini-1.5-flash-latest"),
    mode=instructor.Mode.GEMINI_JSON,
)

AVAILABLE_CATEGORIES: List[str] = [cat.value for cat in Category]

def get_system_prompt(message: str) -> str:
    """Creates a detailed prompt for the Gemini model."""
    return f"""
    **Task**: Triage a customer inquiry.
    
    **Instructions**:
    Your goal is to accurately classify a user's message into one of the predefined categories.
    Analyze the following user message and provide the most likely category, a concise justification for your choice, and a confidence score from 0.0 to 1.0.

    **Available Categories and their criteria**:
    - **TECHNICAL_SUPPORT**: Problems using the product, errors, bugs, performance issues (e.g., "can't log in", "feature not working").
    - **BILLING_INQUIRY**: Questions about invoices, payments, subscriptions, refunds, pricing (e.g., "double charged", "how to get a refund").
    - **SALES**: Pre-purchase inquiries about features, pricing plans, demonstrations (e.g., "do you have feature X?", "what is the enterprise price?").
    - **ACCOUNT_MANAGEMENT**: Requests to update personal information, change plans, cancel accounts (e.g., "change my email", "cancel subscription").
    - **GENERAL_FEEDBACK**: Suggestions, compliments, or general comments not requiring immediate action (e.g., "I love your product", "you should add...").

    **User Message to Analyze**:
    "{message}"
    """

async def triage_message(message: str) -> TriageResponse:
    """
    Uses the Google Gemini API to classify the user's message.
    """
    prompt = get_system_prompt(message)

    try:
        # THE FIX IS HERE: Pass the generation_config as a plain dictionary.
        response = client.chat.completions.create(
            response_model=TriageResponse,
            messages=[
                {"role": "user", "content": prompt}
            ],
            # Pass model-specific arguments as a dictionary, not an object.
            generation_config={"temperature": 0.0}
        )
        return response
    except Exception as e:
        print(f"An error occurred while calling the Gemini API: {e}")
        raise
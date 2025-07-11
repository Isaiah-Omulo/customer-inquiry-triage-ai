# backend/app/models.py

from pydantic import BaseModel, Field
from enum import Enum

class Category(str, Enum):
    """Enumeration for the available triage categories."""
    TECHNICAL_SUPPORT = "TECHNICAL_SUPPORT"
    BILLING_INQUIRY = "BILLING_INQUIRY"
    SALES = "SALES"
    ACCOUNT_MANAGEMENT = "ACCOUNT_MANAGEMENT"
    GENERAL_FEEDBACK = "GENERAL_FEEDBACK"

class TriageRequest(BaseModel):
    """Request model for the /triage endpoint."""
    message: str = Field(
        ...,
        min_length=10,
        description="The customer inquiry message to be triaged.",
        examples=["I can't seem to reset my password, can you help?"]
    )

class TriageResponse(BaseModel):
    """Response model for the /triage endpoint."""
    category: Category = Field(
        ...,
        description="The determined category for the inquiry.",
        examples=[Category.TECHNICAL_SUPPORT]
    )
    reasoning: str = Field(
        ...,
        description="A 1-2 sentence justification for the classification.",
        examples=["The message mentions password reset, which is a common technical support issue."]
    )
    score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="A confidence score between 0.0 (not sure) and 1.0 (certain).",
        examples=[0.95]
    )
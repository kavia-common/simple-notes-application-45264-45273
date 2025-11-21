from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


# PUBLIC_INTERFACE
class ErrorResponse(BaseModel):
    """Standard error payload."""

    detail: str = Field(..., description="Human-readable error message", examples=["Note not found"])
    code: Optional[str] = Field(
        default=None,
        description="Optional machine-friendly error code",
        examples=["not_found", "validation_error"],
    )

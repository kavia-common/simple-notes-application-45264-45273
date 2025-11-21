from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator


# PUBLIC_INTERFACE
class NoteBase(BaseModel):
    """Base fields for a Note."""

    title: str = Field(..., description="Short, non-empty title of the note", examples=["Grocery List"])
    content: str = Field(
        ...,
        description="Full text content of the note. Can be empty if title carries meaning.",
        examples=["- Milk\n- Eggs\n- Bread"],
    )

    @field_validator("title")
    @classmethod
    def validate_title_not_empty(cls, v: str) -> str:
        """Ensure the title is non-empty after trimming spaces."""
        if v is None:
            raise ValueError("title is required")
        t = v.strip()
        if not t:
            raise ValueError("title must not be empty")
        return t


# PUBLIC_INTERFACE
class NoteCreate(NoteBase):
    """Payload model to create a new note."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {"title": "Project Ideas", "content": "1) Build notes app\n2) Learn FastAPI"}
            ]
        }
    }


# PUBLIC_INTERFACE
class NoteUpdate(BaseModel):
    """Payload model to update an existing note; all fields are optional and trimmed if provided."""

    title: Optional[str] = Field(
        default=None,
        description="New title for the note. If provided, must be non-empty after trimming.",
        examples=["Updated Title"],
    )
    content: Optional[str] = Field(
        default=None,
        description="New content for the note.",
        examples=["Updated content body"],
    )

    @field_validator("title")
    @classmethod
    def validate_optional_title(cls, v: Optional[str]) -> Optional[str]:
        """Validate optional title to be non-empty if provided."""
        if v is None:
            return v
        t = v.strip()
        if not t:
            raise ValueError("title must not be empty when provided")
        return t


# PUBLIC_INTERFACE
class Note(NoteBase):
    """Complete Note model with identifiers and timestamps."""

    id: UUID = Field(
        ...,
        description="Unique identifier for the note",
        examples=[str(uuid4())],
    )
    created_at: datetime = Field(
        ...,
        description="Timestamp when the note was created (UTC, ISO 8601)",
        examples=[datetime.now(timezone.utc).isoformat()],
    )
    updated_at: datetime = Field(
        ...,
        description="Timestamp when the note was last updated (UTC, ISO 8601)",
        examples=[datetime.now(timezone.utc).isoformat()],
    )

    @classmethod
    def new(cls, title: str, content: str) -> "Note":
        """
        Create a new Note instance with generated id and timestamps.
        """
        now = datetime.now(timezone.utc)
        return cls(id=uuid4(), title=title, content=content, created_at=now, updated_at=now)

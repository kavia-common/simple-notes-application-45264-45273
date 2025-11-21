from __future__ import annotations

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from src.core.deps import get_notes_service
from src.models.note_models import Note, NoteCreate, NoteUpdate
from src.schemas.error_responses import ErrorResponse
from src.services.notes_service import NotesService, NoteNotFoundError

router = APIRouter(prefix="/api/notes", tags=["notes"])


@router.get(
    "/",
    response_model=List[Note],
    summary="List notes",
    description="Retrieve a paginated list of notes.",
)
def list_notes(
    limit: int = Query(50, ge=1, le=1000, description="Maximum number of notes to return"),
    offset: int = Query(0, ge=0, description="Number of notes to skip from the start"),
    svc: NotesService = Depends(get_notes_service),
):
    """List notes with optional pagination."""
    return svc.list_notes(limit=limit, offset=offset)


@router.get(
    "/{note_id}",
    response_model=Note,
    responses={404: {"model": ErrorResponse, "description": "Note not found"}},
    summary="Get note",
    description="Retrieve a note by its UUID.",
)
def get_note(
    note_id: UUID = Path(..., description="UUID of the note"),
    svc: NotesService = Depends(get_notes_service),
):
    """Return a single Note by id or 404 if not found."""
    try:
        return svc.get_note(note_id)
    except NoteNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Note,
    summary="Create note",
    description="Create a new note with a non-empty title and content.",
)
def create_note(
    payload: NoteCreate,
    svc: NotesService = Depends(get_notes_service),
):
    """Create a new note and return it."""
    return svc.create_note(payload)


@router.put(
    "/{note_id}",
    response_model=Note,
    responses={404: {"model": ErrorResponse, "description": "Note not found"}},
    summary="Update note",
    description="Update an existing note by its UUID. Partial updates are supported.",
)
def update_note(
    note_id: UUID = Path(..., description="UUID of the note"),
    payload: NoteUpdate = ...,
    svc: NotesService = Depends(get_notes_service),
):
    """Update an existing note or return 404 if not found."""
    try:
        return svc.update_note(note_id, payload)
    except NoteNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )


@router.delete(
    "/{note_id}",
    responses={
        200: {
            "description": "Note deleted",
            "content": {"application/json": {"example": {"message": "deleted"}}},
        },
        404: {"model": ErrorResponse, "description": "Note not found"},
    },
    summary="Delete note",
    description="Delete a note by its UUID.",
)
def delete_note(
    note_id: UUID = Path(..., description="UUID of the note"),
    svc: NotesService = Depends(get_notes_service),
):
    """Delete note by id; returns confirmation message or 404."""
    try:
        svc.delete_note(note_id)
        return {"message": "deleted"}
    except NoteNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

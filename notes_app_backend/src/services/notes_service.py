from __future__ import annotations

from typing import List
from uuid import UUID

from src.models.note_models import Note, NoteCreate, NoteUpdate
from src.repositories.memory_notes_repo import MemoryNotesRepository


class NoteNotFoundError(Exception):
    """Raised when a note is not found."""


class NotesService:
    """
    Service layer for manipulating notes.
    Handles trimming, basic validation, and delegates persistence to the repository.
    """

    def __init__(self, repo: MemoryNotesRepository) -> None:
        self._repo = repo

    # PUBLIC_INTERFACE
    def list_notes(self, limit: int = 50, offset: int = 0) -> List[Note]:
        """List notes with pagination parameters forwarded to repository."""
        return self._repo.list_notes(limit=limit, offset=offset)

    # PUBLIC_INTERFACE
    def get_note(self, note_id: UUID) -> Note:
        """Retrieve a note by id or raise NoteNotFoundError."""
        note = self._repo.get_note(note_id)
        if not note:
            raise NoteNotFoundError(f"Note {note_id} not found")
        return note

    # PUBLIC_INTERFACE
    def create_note(self, data: NoteCreate) -> Note:
        """
        Create a new note.
        Trims title and relies on Pydantic validations for non-empty titles.
        """
        normalized = NoteCreate(title=data.title.strip(), content=data.content)
        return self._repo.create_note(normalized)

    # PUBLIC_INTERFACE
    def update_note(self, note_id: UUID, data: NoteUpdate) -> Note:
        """
        Update an existing note; trims title if provided.
        Raises NoteNotFoundError if the note does not exist.
        """
        normalized = NoteUpdate(
            title=(data.title.strip() if data.title is not None else None),
            content=data.content,
        )
        updated = self._repo.update_note(note_id, normalized)
        if not updated:
            raise NoteNotFoundError(f"Note {note_id} not found")
        return updated

    # PUBLIC_INTERFACE
    def delete_note(self, note_id: UUID) -> None:
        """Delete note by id or raise NoteNotFoundError if not found."""
        ok = self._repo.delete_note(note_id)
        if not ok:
            raise NoteNotFoundError(f"Note {note_id} not found")

from __future__ import annotations

from threading import RLock
from typing import Dict, List, Optional
from uuid import UUID

from datetime import datetime, timezone

from src.models.note_models import Note, NoteCreate, NoteUpdate


class MemoryNotesRepository:
    """
    Thread-safe in-memory repository for Notes using a dictionary keyed by UUID.
    Not intended for production use; serves as a simple persistence layer for demo/testing.
    """

    def __init__(self) -> None:
        self._lock = RLock()
        self._notes: Dict[UUID, Note] = {}

    # PUBLIC_INTERFACE
    def list_notes(self, limit: int = 50, offset: int = 0) -> List[Note]:
        """List notes with simple pagination."""
        with self._lock:
            items = list(self._notes.values())
            # Stable order by created_at then id for deterministic behavior
            items.sort(key=lambda n: (n.created_at, str(n.id)))
            return items[offset : offset + limit]

    # PUBLIC_INTERFACE
    def get_note(self, note_id: UUID) -> Optional[Note]:
        """Get a note by id or return None if not found."""
        with self._lock:
            return self._notes.get(note_id)

    # PUBLIC_INTERFACE
    def create_note(self, data: NoteCreate) -> Note:
        """Create and store a new note."""
        with self._lock:
            note = Note.new(title=data.title.strip(), content=data.content)
            self._notes[note.id] = note
            return note

    # PUBLIC_INTERFACE
    def update_note(self, note_id: UUID, data: NoteUpdate) -> Optional[Note]:
        """Update an existing note if found; returns updated Note or None."""
        with self._lock:
            existing = self._notes.get(note_id)
            if not existing:
                return None

            updated_title = existing.title
            updated_content = existing.content

            if data.title is not None:
                updated_title = data.title.strip()

            if data.content is not None:
                updated_content = data.content

            updated = Note(
                id=existing.id,
                title=updated_title,
                content=updated_content,
                created_at=existing.created_at,
                updated_at=datetime.now(timezone.utc),
            )
            self._notes[note_id] = updated
            return updated

    # PUBLIC_INTERFACE
    def delete_note(self, note_id: UUID) -> bool:
        """Delete a note by id; returns True if deleted, False if not found."""
        with self._lock:
            if note_id in self._notes:
                del self._notes[note_id]
                return True
            return False

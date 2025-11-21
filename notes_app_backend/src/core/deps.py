from __future__ import annotations

from functools import lru_cache

from src.repositories.memory_notes_repo import MemoryNotesRepository
from src.services.notes_service import NotesService


@lru_cache(maxsize=1)
def _singleton_repo() -> MemoryNotesRepository:
    """
    Internal singleton instance of the in-memory repository.
    Using lru_cache for simple module-level singleton semantics.
    """
    return MemoryNotesRepository()


# PUBLIC_INTERFACE
def get_notes_service() -> NotesService:
    """
    FastAPI dependency that yields a NotesService backed by a singleton repository.
    """
    return NotesService(repo=_singleton_repo())

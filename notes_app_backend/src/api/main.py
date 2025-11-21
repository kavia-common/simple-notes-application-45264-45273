from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers.notes import router as notes_router

app = FastAPI(
    title="Simple Notes API",
    description="A minimal Notes CRUD API implemented with FastAPI and in-memory persistence.",
    version="1.0.0",
    contact={"name": "Notes API", "url": "https://example.com"},
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For demo purposes; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", summary="Health Check", tags=["health"])
def health_check():
    """Simple liveness check endpoint."""
    return {"message": "Healthy"}


# Routers
app.include_router(notes_router)

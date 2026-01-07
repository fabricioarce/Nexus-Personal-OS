from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from backend.app.modules.journal.api import diary, chat, stats
from backend.app.modules.eisenhower import router as eisenhower
from backend.app.core.exceptions import global_exception_handler

app = FastAPI(title="Nexus Personal OS API")

@app.on_event("startup")
def on_startup():
    from backend.app.core.database import init_db
    # Need to import models here to ensure they are registered with SQLModel
    from backend.app.modules.journal import models as journal_models
    from backend.app.modules.eisenhower import models as eisenhower_models
    init_db()

app.add_exception_handler(Exception, global_exception_handler)

app.include_router(diary.router, prefix="/api/journal/diary")
app.include_router(chat.router, prefix="/api/journal/chat")
app.include_router(stats.router, prefix="/api/journal/stats")
app.include_router(eisenhower.router, prefix="/api/eisenhower")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4321", "http://localhost:8000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir el frontend compilado
frontend_path = os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
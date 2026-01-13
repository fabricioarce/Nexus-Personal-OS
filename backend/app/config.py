from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Raíz del proyecto (Diario/)
BASE_DIR = Path(__file__).resolve().parents[2]

# data/
DATA_DIR = BASE_DIR / "data"

# diary/
DIARY_DIR = DATA_DIR / "diary"

# ── ENTRADAS ──────────────────────────────

# Entradas originales en markdown
DIARY_ENTRIES_DIR = DIARY_DIR / "entries"

# JSON crudo (si lo usás como fuente)
RAW_DIR = DATA_DIR / "raw"
RAW_DIARY_JSON = RAW_DIR / "diario.json"

# ── PROCESADOS (SALIDA) ───────────────────

PROCESSED_DIR = DIARY_DIR / "processed"

CHUNKS_FILE = PROCESSED_DIR / "chunks.json"
METADATA_FILE = PROCESSED_DIR / "metadata.json"
FAISS_INDEX_FILE = PROCESSED_DIR / "index.faiss"

# ── DATABASE ─────────────────────────────
import os
DATABASE_PATH = DATA_DIR / "diario.db"
# Prioridad: Variable de entorno (Render/Railway) > SQLite local
DATABASE_URL = os.environ.get("DATABASE_URL", f"sqlite:///{DATABASE_PATH}")

# Fix para Render/Railway (devuelven postgres:// pero SQLAlchemy quiere postgresql://)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

from datetime import date
from pathlib import Path

DIARY_PATH = Path("data/diary/entries")
DIARY_PATH.mkdir(parents=True, exist_ok=True)

def save_entry(text: str):
    today = date.today().isoformat()
    path = DIARY_PATH / f"{today}.md"
    path.write_text(text, encoding="utf-8")

def list_entries():
    return sorted(p.stem for p in DIARY_PATH.glob("*.md"))

def read_entry(date: str):
    path = DIARY_PATH / f"{date}.md"
    if not path.exists():
        return {"error": "not found"}
    return {"date": date, "text": path.read_text(encoding="utf-8")}

import sys
import os

# Añadir el directorio raíz al path para que los imports funcionen
sys.path.append(os.getcwd())

from backend.app.core.database import init_db, engine
from sqlmodel import SQLModel

# Importar modelos para que SQLModel los reconozca
from backend.app.modules.journal import models as journal_models
from backend.app.modules.eisenhower import models as eisenhower_models
from backend.app.modules.retroplanning import models as retro_models
from backend.app.modules.profile import models as profile_models

def main():
    print(f"Connecting to database...")
    init_db()
    print("Database tables created successfully!")

if __name__ == "__main__":
    main()

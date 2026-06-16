import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database" / "opria.db"

JWT_SECRET = os.getenv("OPRIA_JWT_SECRET", "opria-dev-secret-change-me")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = int(os.getenv("OPRIA_JWT_EXPIRATION_HOURS", "8"))

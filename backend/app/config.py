import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
KAMUS_PATH = DATA_DIR / "kamus.json"

BACKEND_HOST = os.getenv("BACKEND_HOST", "127.0.0.1")
BACKEND_PORT = int(os.getenv("BACKEND_PORT", "8000"))

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000").rstrip("/")

APP_NAME = "AutoKey"
APP_VERSION = "0.1.0"
APP_DESCRIPTION = (
    "Web-based Indonesian text editor with autocomplete and spell checking."
)
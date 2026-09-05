import os
import sys
from pathlib import Path


if getattr(sys, "frozen", False):
    APP_DIR = Path(sys._MEIPASS)

    DATA_DIR = (
        Path(os.environ.get("PROGRAMDATA", Path.home()))
        / "ANDRITZ"
        / "ProdDashMCMS"
        / "data"
    )

    FRONTEND_DIR = APP_DIR / "frontend"

else:
    BACKEND_DIR = Path(__file__).resolve().parent
    PROJECT_DIR = BACKEND_DIR.parent

    APP_DIR = BACKEND_DIR
    DATA_DIR = BACKEND_DIR / "data"
    FRONTEND_DIR = PROJECT_DIR / "frontend" / "dist"


DATA_DIR.mkdir(parents=True, exist_ok=True)

LOGO_PATH = APP_DIR / "reports" / "assets" / "logo_metris_wave.png"
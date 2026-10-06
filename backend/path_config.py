import os
import sys
from pathlib import Path

if getattr(sys, "frozen", False):
    APP_DIR = Path(sys._MEIPASS)

    configured_data_dir = os.environ.get("PRODDASH_DATA_DIR")

    if configured_data_dir:
        DATA_DIR = Path(configured_data_dir)
    else:
        DATA_DIR = (
            Path(os.environ.get("PROGRAMDATA", Path.home()))
            / "ANDRITZ"
            / "ProdDashECMS"
            / "data"
        )

    FRONTEND_DIR = APP_DIR / "frontend"

else:
    BACKEND_DIR = Path(__file__).resolve().parent
    PROJECT_DIR = BACKEND_DIR.parent

    APP_DIR = BACKEND_DIR
    
    configured_data_dir = os.environ.get("PRODDASH_DATA_DIR")

    if configured_data_dir:
        DATA_DIR = Path(configured_data_dir)
    else:
        DATA_DIR = BACKEND_DIR / "data"

    FRONTEND_DIR = PROJECT_DIR / "frontend" / "dist"


DATA_DIR.mkdir(parents=True, exist_ok=True)

LOGO_PATH = APP_DIR / "reports" / "assets" / "logo_metris_wave.png"
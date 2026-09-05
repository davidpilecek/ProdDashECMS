from waitress import serve

from app import create_app
from path_config import FRONTEND_DIR

app = create_app(frontend_dir=FRONTEND_DIR)

if __name__ == "__main__":
    serve(
        app,
        host="127.0.0.1",
        port=5000,
        threads=8,
    )
import argparse
import os
# These imports must happen after PRODDASH_DATA_DIR is set.
from waitress import serve
from app import create_app
from path_config import FRONTEND_DIR, DATA_DIR

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--port",
        type=int,
        default=5003,
    )

    parser.add_argument(
        "--data-dir",
        type=str,
        default=None,
    )

    args = parser.parse_args()

    # Set the data directory BEFORE importing the Flask application.
    if args.data_dir:
        os.environ["PRODDASH_DATA_DIR"] = args.data_dir

    print(f"Starting ProdDashECMS")
    print(f"Port: {args.port}")
    print(f"Data directory: {DATA_DIR}")

    app = create_app(frontend_dir=FRONTEND_DIR)

    serve(
        app,
        host="127.0.0.1",
        port=args.port,
        threads=8,
    )

if __name__ == "__main__":
    main()
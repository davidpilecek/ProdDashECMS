from pathlib import Path

from flask import Flask, send_from_directory
from flask_cors import CORS

from routes.report import report_bp
from routes.production import production_bp
from routes.statistics import statistics_bp

def create_app(frontend_dir=None):
    app = Flask(__name__)

    CORS(app)

    # Register API blueprints
    app.register_blueprint(production_bp)
    app.register_blueprint(statistics_bp)
    app.register_blueprint(report_bp)

    @app.get("/api/health")
    def health():
        return {"status": "ok"}

    # Only enable this when a production frontend directory
    # is supplied.
    if frontend_dir is not None:
        frontend_dir = Path(frontend_dir)

        @app.route("/", defaults={"path": ""})
        @app.route("/<path:path>")
        def serve_frontend(path):
            requested_file = frontend_dir / path

            if requested_file.is_file():
                return send_from_directory(frontend_dir, path)

            return send_from_directory(frontend_dir, "index.html")

    return app


# Development application
app = create_app()


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
    )
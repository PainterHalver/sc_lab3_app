from flask import Flask, send_from_directory
import os
from flask_cors import CORS
from controllers.security_groups import security_groups_bp
from controllers.csv import csv_bp
from config import DATABASE_URI, DEBUG
from models import db


def create_app():
    app = Flask(__name__, static_folder="client/build")
    CORS(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    app.debug = DEBUG
    db.init_app(app)

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve(path):
        if path != "" and os.path.exists(app.static_folder + "/" + path):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, "index.html")

    @app.route("/health")
    def health():
        return "OK"

    app.register_blueprint(security_groups_bp)
    app.register_blueprint(csv_bp)
    setup_database(app)
    return app


def setup_database(app):
    with app.app_context():
        db.create_all()


if __name__ == "__main__":
    app = create_app()
    app.run()

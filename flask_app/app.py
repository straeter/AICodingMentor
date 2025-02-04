import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_app.config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder="templates")

    app.config.from_object(Config)

    db.init_app(app)

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Flask app starting")

    from flask_app.routes import main as main_bp
    app.register_blueprint(main_bp)

    from flask_app.simple_db import Challenge

    with app.app_context():
        db.create_all()

    return app

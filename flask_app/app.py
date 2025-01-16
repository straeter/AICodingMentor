import logging

from flask import Flask

from flask_app.config import Config


def create_app(model="gpt-4o-mini"):
    app = Flask(__name__, template_folder="templates")

    app.config.from_object(Config)

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Flask app starting")

    from flask_app.routes import main as main_bp
    app.register_blueprint(main_bp)

    return app

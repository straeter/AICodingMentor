import inspect
import logging

from flask import Flask

from flask_app.config import Config
from flask_app.utils import jinja_templates

functions = inspect.getmembers(jinja_templates, inspect.isfunction)


def create_app(model="gpt-4o-mini"):
    app = Flask(__name__, template_folder="templates")

    app.config.from_object(Config)

    # Flask Logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Flask app starting")

    from flask_app.routes import main as main_bp
    app.register_blueprint(main_bp)

    # Add the filter function to the Jinja2 environment
    for name, func in functions:
        app.jinja_env.filters[name] = func

    return app

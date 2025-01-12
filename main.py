import argparse

from flask_app.app import create_app
import os


def main(debug=False):
    app = create_app()

    app.run(debug=debug, host='0.0.0.0', port=5000)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run main app to manage issues.")
    parser.add_argument("--debug", action="store_true", default=False, help="if run in debug mode")
    args = parser.parse_args()

    main(debug=args.debug)

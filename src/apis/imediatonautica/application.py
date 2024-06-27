"""API flask application factory module."""

from collections import deque
from importlib import import_module, resources
from flask import Blueprint, Flask
from logging.config import dictConfig
from flask_cors import CORS
import awsgi

from config import Config 
from chats.views import app as chats_blueprint  # Import the chats blueprint directly for simplicity

def create_app():
    """Create and initialize a API flask application."""

    if hasattr(config, 'LOGGING'):
        dictConfig(config.LOGGING)

    app = create_flask_app()
    CORS(app, resources={r"/*": {"origins": "*", "allow_headers": "*"}})  # Initialize CORS here

    return app

def create_flask_app():
    """
    Create a Flask application.

    :param config: Configuration to use.
    :return: A Flask app.
    """
    app = Flask(__name__)
    app.env = config.APP_ENV
    app.config.from_object(config)

    # Register the blueprint directly for simplicity
    # register_blueprints(app, 'imediatonautica')
    #TODO: Fix the automatic register of blueprints. Not Getting the defined methods
    app.register_blueprint(chats_blueprint)  # Register the chats blueprint here

    return app

def register_blueprints(app: Flask, package: str):
    """
    Register the flask.Blueprint instance from inside a package to a flask app.

    This will only register blueprints that are inside a submodule named 'views.py'.

    :param app: The Flask app to register the blueprints in.
    :param package: The package str representation (__package__) to look for Blueprint instances.
    """
    print(f'Registering blueprints from package: {package}')
    modules = deque([package])
    while modules:
        module = modules.popleft()
        for resource in resources.files(module).iterdir():
            if not resource.is_file():
                modules.append(f'{module}.{resource.name}')
            elif resource.name == 'views.py':
                views = import_module(f'{module}.views')
                for item in dir(views):
                    obj = getattr(views, item)
                    if isinstance(obj, Blueprint):
                        print(f'Registering blueprint: {obj.name}')
                        app.register_blueprint(obj)  # Register the blueprint here

config = Config()
application = create_app()

def main():
    application.run(debug=config.DEBUG)

def lambda_handler(event, context):
    return awsgi.response(application, event, context)

if __name__ == "__main__":
    main()

import os

from Crypto.Random import get_random_bytes
from flask import Flask
from flask_cors import CORS
from flask_oidc import OpenIDConnect, discovery, registration

from .config import Config

oidc = OpenIDConnect()

def create_app(test_config=None):
    # Create and configure app
    app = Flask(__name__, instance_relative_config=True)
    if os.getenv('FLASK_ENV') == "development":
        app.secret_key = "heisann"      
    else:
        app.secret_key = get_random_bytes(32)
    # 
    # CORS implemented so that we don't get errors when trying to access the server from a different server location
    CORS(app)
    
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object(Config)
        app.config["DATABASE"] = os.path.join(app.instance_path, "behaviourmapper.db")
        app.config.from_mapping(
        OIDC_CLIENT_SECRETS=os.path.join(Config.STATIC_URL_PATH, 'client_secrets.json'),      
        OIDC_CALLBACK_ROUTE= '/behaviourmapper',
        )
        if os.getenv('FLASK_ENV') == "development":
            app.config.from_mapping(OIDC_COOKIE_SECURE=False)
        oidc.init_app(app)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import errorhandlers
    app.register_error_handler(errorhandlers.InvalidUsage ,errorhandlers.handle_invalid_usage)

    from . import routes
    app.register_blueprint(routes.bp)

    from . import db
    db.init_app(app)

    return app


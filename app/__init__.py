from flask import Flask
from .db import close_db

def create_app():
    app = Flask(__name__)

    # Chemin de la DB SQLite dans instance/
    app.config["DB_PATH"] = "instance/owasp_academy.sqlite"

    from .routes import main
    app.register_blueprint(main)

    # Fermer proprement la DB à la fin de chaque requête
    app.teardown_appcontext(close_db)

    return app

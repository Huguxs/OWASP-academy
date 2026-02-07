import sqlite3
from pathlib import Path
from flask import current_app, g

def get_db():
    # 1 connexion SQLite par requête (pattern Flask classique)
    if "db" not in g:
        db_path = Path(current_app.config["DB_PATH"])
        db_path.parent.mkdir(parents=True, exist_ok=True)
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row  # pour accéder aux colonnes par nom
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

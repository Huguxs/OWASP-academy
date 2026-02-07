import sqlite3
import hashlib
from pathlib import Path

DB_PATH = Path("instance/owasp_academy.sqlite")

def md5_hex(s: str) -> str:
    return hashlib.md5(s.encode("utf-8")).hexdigest()

def main():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_md5 TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'user'
    );
    """)

    # Tes mots de passe (hashés en MD5)
    admin_pw = "soccer11"
    alice_pw = "H7(q-X;F;U-g^.l4+A@<"

    cur.execute(
        "INSERT OR IGNORE INTO users (username, password_md5, role) VALUES (?, ?, ?)",
        ("admin", md5_hex(admin_pw), "admin")
    )
    cur.execute(
        "INSERT OR IGNORE INTO users (username, password_md5, role) VALUES (?, ?, ?)",
        ("alice", md5_hex(alice_pw), "user")
    )

    conn.commit()

    rows = cur.execute("SELECT id, username, role FROM users").fetchall()
    print("[OK] Users dans la DB :")
    for r in rows:
        print(f" - id={r[0]} username={r[1]} role={r[2]}")

    conn.close()
    print(f"[OK] DB initialisée: {DB_PATH}")

if __name__ == "__main__":
    main()

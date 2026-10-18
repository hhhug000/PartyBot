import sqlite3
from contextlib import contextmanager

db = "partybot.db"

@contextmanager
def get_db():
    conn = sqlite3.connect(db)
    try:
        yield conn
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def add_score(user_id, score):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM scores WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        if result is None:
            cursor.execute("INSERT INTO scores (user_id, score) VALUES (?, ?)", (user_id, score))
            conn.commit()
        else:
            cursor.execute("UPDATE scores SET score = score + ? WHERE user_id = ?", (score, user_id))
            conn.commit()

def get_leaderboard():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, score FROM scores ORDER BY score DESC LIMIT 5")
        return cursor.fetchall()

def get_score(user_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT score FROM scores WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        if result is None:
            return 0
        return result[0]

def setup_db():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                user_id INTEGER PRIMARY KEY,
                score INTEGER NOT NULL
            )
        """)
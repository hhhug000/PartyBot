import os
import random
import sqlite3
import json
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

def get_trivia_categories():
    files = os.listdir("trivia-dataset")
    for i, file in enumerate(files):
        files[i] = file.replace(".json", "")
    return files

def get_trivia_questions(category):
    with open(f"trivia-dataset/{category}.json", "r", encoding="utf-8") as f:
        data = f.read()
        questions = json.loads(data)
        valid_questions = [
            question
            for question in questions
            if question.get("question")
            and question.get("answer") in question.get("choices", [])
            and 2 <= len(question.get("choices", [])) <= 4
        ]
        if not valid_questions:
            raise ValueError(f"No valid trivia questions found for category: {category}")
        question = random.choice(valid_questions)
        questiontext = question["question"]
        answer = question["answer"]
        possibleanswers = question["choices"]
        return questiontext, answer, possibleanswers
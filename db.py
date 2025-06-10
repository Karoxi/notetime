import sqlite3
from datetime import datetime
import random

def init_db():
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        date TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

def create_note(note):
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        date TEXT NOT NULL
    )
    ''')
    cursor.execute("INSERT INTO notes (text, date) VALUES (?, ?)", (note, datetime.now().strftime("%d-%m-%Y")))
    conn.commit()
    conn.close()

def get_random_note():
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT text, date FROM notes")
    all_notes = cursor.fetchall()
    conn.close()
    if all_notes:
        return random.choice(all_notes)
    return None

def get_all_notes():
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, text, date FROM notes ORDER BY id DESC")
    all_notes = cursor.fetchall()
    conn.close()
    return all_notes

def delete_all_notes():
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes")
    conn.commit()
    conn.close()
    
def delete_note_by_id(note_id):
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()

def update_note_by_id(note_id, new_text):
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE notes SET text = ? WHERE id = ?", (new_text, note_id))
    conn.commit()
    conn.close()


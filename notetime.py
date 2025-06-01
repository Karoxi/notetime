import sqlite3
from datetime import datetime
import random

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
def show_note():
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT text, date FROM notes")
    all_notes = cursor.fetchall()
    note = random.choice(all_notes)
    print(f"\n📅 {note[1]} – 📝 {note[0]}\n")
    conn.close()
def delete_all_notes():
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes")
    conn.commit()
    conn.close()


if __name__ == "__main__":
    note = input("What did you learn today?")
    create_note(note)
    show_note()
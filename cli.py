from db import create_note, get_random_note, init_db

def run_cli():
    init_db()
    note = input("What did you learn today? ")
    if note:
        create_note(note)
        random_note = get_random_note()
        if random_note:
            print(f"\n📅 {random_note[1]} – 📝 {random_note[0]}\n")
        else:
            print("No notes found.")

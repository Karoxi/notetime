import tkinter as tk
from tkinter import messagebox, font
import db

def run_gui():
    db.init_db()

    root = tk.Tk()
    root.title("NoteTime")
    root.geometry("600x600")
    root.configure(bg="#fffde7")  # Sanftes Gelb

    default_font = font.nametofont("TkDefaultFont")
    default_font.configure(size=11)

    # Titel
    header = tk.Label(root, text="NoteTime", bg="#fffde7", fg="#f9a825", font=("Segoe UI", 24, "bold"))
    header.pack(pady=(20, 10))

    # Texteingabe
    entry = tk.Text(root, height=5, font=("Segoe UI", 12), wrap="word", bd=2, relief="groove", fg="gray")
    entry.insert("1.0", "What did you learn today?")
    entry.pack(padx=20, pady=(0, 5), fill="x")

    def on_entry_click(event):
        if entry.get("1.0", "end-1c") == "What did you learn today?":
            entry.delete("1.0", "end")
            entry.configure(fg="black")

    def on_focusout(event):
        if entry.get("1.0", "end-1c").strip() == "":
            entry.insert("1.0", "What did you learn today?")
            entry.configure(fg="gray")

    entry.bind('<FocusIn>', on_entry_click)
    entry.bind('<FocusOut>', on_focusout)

    # Statusanzeige
    status_label = tk.Label(root, text="", bg="#fffde7", fg="#f57f17", font=("Segoe UI", 10))
    status_label.pack()

    def add_note():
        text = entry.get("1.0", "end-1c").strip()
        if text and text != "What did you learn today?":
            db.create_note(text)
            entry.delete("1.0", "end")
            status_label.config(text="Successfully added new note.", fg="#388e3c")
            refresh_random_note()
        else:
            status_label.config(text="Note is empty.", fg="red")

    add_btn = tk.Button(root, text="Add Note", command=add_note,
                        bg="#fdd835", fg="black", font=("Segoe UI", 11),
                        relief="flat", activebackground="#fbc02d")
    add_btn.pack(pady=(10, 15), ipadx=10, ipady=5)

    # Zufallsnotiz
    random_note_label = tk.Label(root, text="", bg="#fffde7",
                                 fg="#5d4037", font=("Segoe UI", 12, "italic"),
                                 wraplength=500, justify="center")
    random_note_label.pack(pady=(0, 5), fill="x")

    def refresh_random_note():
        note = db.get_random_note()
        if note:
            random_note_label.config(text=f"Today's random note:\n📅 {note[1]} – 📝 {note[0]}")
        else:
            random_note_label.config(text="No notes available yet.")

    refresh_btn = tk.Button(root, text="🔄", command=refresh_random_note,
                            bg="#fdd835", fg="black", font=("Segoe UI", 14),
                            relief="flat", width=3, activebackground="#fbc02d")
    refresh_btn.pack(pady=(0, 20))

    refresh_random_note()

    # Organize Notes Button öffnet ein separates Fenster
    def open_organizer_window():
        organizer = tk.Toplevel(root)
        organizer.title("Your Notes")
        organizer.geometry("600x400")
        organizer.configure(bg="#fffde7")

        outer_frame = tk.Frame(organizer, bg="#fffde7")
        outer_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(outer_frame, bg="#fffde7", highlightthickness=0)
        scrollbar = tk.Scrollbar(outer_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#fffde7")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas_frame = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Mausrad scrollen
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        def refresh_notes():
            for widget in scrollable_frame.winfo_children():
                widget.destroy()

            notes = db.get_all_notes()
            if not notes:
                tk.Label(scrollable_frame, text="No notes available.", bg="#fffde7",
                         fg="#5d4037", font=("Segoe UI", 12)).pack(pady=10)
                return

            for note in notes:
                note_text = f"📅 {note[2]} – 📝 {note[1]}"
                note_frame = tk.Frame(scrollable_frame, bg="#fff9c4", pady=5, padx=10)
                note_frame.pack(fill="x", pady=4)

                label = tk.Label(note_frame, text=note_text, anchor="w", justify="left",
                                 bg="#fff9c4", fg="#5d4037", font=("Segoe UI", 11), wraplength=440)
                label.pack(side="left", padx=5, expand=True, fill="x")

                edit_button = tk.Button(note_frame, text="🖊️", command=lambda n=note: edit_note_window(n[0], n[1]),
                                        bg="#fdd835", fg="black", relief="flat", width=3,
                                        activebackground="#fbc02d")
                edit_button.pack(side="right", padx=5)

                del_button = tk.Button(note_frame, text="🗑️", command=lambda n_id=note[0]: delete_note(n_id, refresh_notes),
                                       bg="#fdd835", fg="black", relief="flat", width=3,
                                       activebackground="#fbc02d")
                del_button.pack(side="right", padx=5)

        refresh_notes()

    organize_btn = tk.Button(root, text="🗂️ Organize Notes", command=open_organizer_window,
                             bg="#fdd835", fg="black", font=("Segoe UI", 11),
                             relief="flat", activebackground="#fbc02d")
    organize_btn.pack(pady=(0, 10), ipadx=10, ipady=5)

    def delete_note(note_id, refresh_callback=None):
        db.delete_note_by_id(note_id)
        refresh_random_note()
        if refresh_callback:
            refresh_callback()

    def edit_note_window(note_id, old_text):
        def save_edit():
            new_text = edit_text.get("1.0", "end-1c").strip()
            if new_text:
                db.update_note_by_id(note_id, new_text)
                edit_win.destroy()
                refresh_random_note()
            else:
                messagebox.showwarning("Error", "Note cannot be empty.")

        edit_win = tk.Toplevel(root)
        edit_win.title("Edit Note")
        edit_win.geometry("400x200")
        edit_win.configure(bg="#fffde7")

        tk.Label(edit_win, text="Edit note:", bg="#fffde7", fg="#5d4037", font=("Segoe UI", 12)).pack(pady=10)
        edit_text = tk.Text(edit_win, height=5, font=("Segoe UI", 11), wrap="word", bd=2, relief="groove")
        edit_text.pack(padx=10, pady=5, fill="both", expand=True)
        edit_text.insert("1.0", old_text)

        tk.Button(edit_win, text="Save", command=save_edit, bg="#fdd835", fg="black",
                  relief="flat", font=("Segoe UI", 11), activebackground="#fbc02d").pack(pady=10, ipadx=10, ipady=5)

    root.mainloop()


import tkinter as tk
from tkinter import messagebox
import sqlite3
import random

DB_NAME = "it_adventure.db"

# Each question stores the correct answer separately.
ROOMS = {
    "IT Basics": [
        ("What does IT stand for?", ["Information Technology", "Internet Transfer", "Internal Text"], 0),
        ("Which one is an input device?", ["Monitor", "Keyboard", "Speaker"], 1),
        ("What does CPU mean?", ["Central Processing Unit", "Computer Power User", "Control Program Unit"], 0),
        ("Which device prints documents?", ["Printer", "Mouse", "Router"], 0),
        ("Which one is an operating system?", ["Windows", "Python", "HTML"], 0),
    ],
    "Python": [
        ("What is the output of print('Hello')?", ["Hello", "print", "Error"], 0),
        ("Which symbol is used for comments in Python?", ["//", "#", "/*"], 1),
        ("Which data type stores whole numbers?", ["str", "int", "list"], 1),
        ("Which command gets input from the user?", ["input()", "print()", "write()"], 0),
        ("Which keyword checks a condition?", ["for", "if", "def"], 1),
    ],
    "Networking": [
        ("Which device connects different networks?", ["Router", "Keyboard", "Monitor"], 0),
        ("What is the main purpose of a computer network?", ["Connect devices", "Draw pictures", "Edit videos"], 0),
        ("What does IP stand for?", ["Internet Protocol", "Internal Program", "Input Port"], 0),
        ("Which device commonly connects devices in a LAN?", ["Switch", "Printer", "Scanner"], 0),
        ("What does LAN mean?", ["Local Area Network", "Large Access Number", "Long Area Node"], 0),
    ],
    "Database": [
        ("What is a database?", ["An organized collection of data", "A computer screen", "A programming keyboard"], 0),
        ("What is a table made of?", ["Rows and columns", "Pictures only", "Sounds"], 0),
        ("What does SQL help us do?", ["Work with databases", "Browse photos", "Create animations"], 0),
        ("What is a record in a table?", ["A row of related data", "A column title", "A computer cable"], 0),
        ("Which one is a database system?", ["SQLite", "Paint", "Calculator"], 0),
    ],
}

ROOM_COLORS = {
    "IT Basics": "#4d91d2",
    "Python": "#9b70c8",
    "Networking": "#45a98d",
    "Database": "#e69a4b",
}
ROOM_ICONS = {"IT Basics": "🖥️", "Python": "🐍", "Networking": "🌐", "Database": "🗄️"}


class ITAdventure:
    def __init__(self, root):
        self.root = root
        self.root.title("IT Adventure - Learn & Explore")
        self.root.geometry("1000x720")
        self.root.minsize(820, 620)
        self.root.configure(bg="#dceeff")
        self.name = ""
        self.character = "🧑‍🚀"
        self.score = 0
        self.room = ""
        self.q_index = 0
        self.room_score = 0
        self.current_options = []
        self.correct_display_index = None
        self.answered = False
        self.show_welcome()

    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    def button(self, parent, text, command, color="#2878c8", width=None):
        return tk.Button(
            parent, text=text, command=command, width=width,
            font=("Arial", 12, "bold"), bg=color, fg="white",
            activebackground=color, activeforeground="white",
            relief="flat", bd=0, padx=18, pady=11,
            cursor="hand2", highlightthickness=0
        )

    def title(self, parent, text, size=27, color="#203653"):
        return tk.Label(parent, text=text, font=("Arial", size, "bold"),
                        bg=parent.cget("bg"), fg=color)

    def make_header(self, parent, subtitle):
        top = tk.Frame(parent, bg="#24466b", height=64)
        top.pack(fill="x")
        top.pack_propagate(False)
        tk.Label(top, text="✦  IT ADVENTURE", font=("Arial", 20, "bold"),
                 bg="#24466b", fg="white").pack(side="left", padx=24, pady=13)
        tk.Label(top, text=subtitle, font=("Arial", 11, "bold"),
                 bg="#24466b", fg="#dceeff").pack(side="right", padx=24)

    def show_welcome(self):
        self.clear()
        self.root.configure(bg="#dceeff")
        self.make_header(self.root, "LEARN • EXPLORE • WIN")
        body = tk.Frame(self.root, bg="#dceeff")
        body.pack(expand=True, fill="both", padx=28, pady=24)

        left = tk.Frame(body, bg="#b8dcf4", padx=25, pady=25,
                        highlightbackground="#8bb9dc", highlightthickness=2)
        left.pack(side="left", fill="both", expand=True, padx=(0, 14))
        self.title(left, "WELCOME, EXPLORER!", 25).pack(pady=(15, 5))
        tk.Label(left, text="Your technology adventure starts here.",
                 font=("Arial", 13), bg="#b8dcf4", fg="#36516b").pack(pady=5)

        # Simple cartoon landscape made from Canvas shapes.
        art = tk.Canvas(left, width=390, height=270, bg="#b8dcf4",
                        highlightthickness=0)
        art.pack(pady=15)
        art.create_oval(295, 15, 355, 75, fill="#ffd36a", outline="")
        art.create_rectangle(0, 205, 390, 270, fill="#80c98d", outline="")
        for x, y in [(25, 65), (290, 105), (75, 130)]:
            art.create_oval(x, y, x+65, y+30, fill="white", outline="")
            art.create_oval(x+20, y-12, x+55, y+25, fill="white", outline="")
        art.create_polygon(125, 205, 125, 120, 195, 65, 265, 120, 265, 205,
                           fill="#f3b75d", outline="#9a6937", width=3)
        art.create_polygon(112, 123, 195, 53, 278, 123, fill="#d96f62",
                           outline="#9a4b48", width=3)
        art.create_rectangle(177, 150, 213, 205, fill="#76523e", outline="#593c30", width=2)
        art.create_rectangle(143, 137, 168, 164, fill="#aee5f5", outline="#4f829b", width=2)
        art.create_rectangle(224, 137, 249, 164, fill="#aee5f5", outline="#4f829b", width=2)
        art.create_text(195, 235, text="THE WORLD OF IT", font=("Arial", 13, "bold"),
                        fill="#24513b")

        right = tk.Frame(body, bg="white", padx=30, pady=28,
                         highlightbackground="#c5d8e8", highlightthickness=2)
        right.pack(side="right", fill="y")
        self.title(right, "Create your player", 21).pack(pady=(20, 25))
        tk.Label(right, text="Your name", font=("Arial", 12, "bold"),
                 bg="white", fg="#36516b").pack(anchor="w")
        self.name_entry = tk.Entry(right, font=("Arial", 15), width=22,
                                   justify="center", relief="solid", bd=1)
        self.name_entry.pack(pady=(8, 20), ipady=7)
        tk.Label(right, text="Choose your explorer", font=("Arial", 12, "bold"),
                 bg="white", fg="#36516b").pack()
        self.char_var = tk.StringVar(value="Boy")
        tk.Radiobutton(right, text="🧑‍🚀  Boy", variable=self.char_var, value="Boy",
                       font=("Arial", 13), bg="white").pack(anchor="w", pady=8)
        tk.Radiobutton(right, text="👩‍🚀  Girl", variable=self.char_var, value="Girl",
                       font=("Arial", 13), bg="white").pack(anchor="w", pady=8)
        self.button(right, "START ADVENTURE  ➜", self.start, "#239b68").pack(fill="x", pady=(25, 10))
        tk.Label(right, text="4 rooms  •  20 questions  •  1 big adventure",
                 font=("Arial", 9), bg="white", fg="#71849a").pack(pady=8)

    def start(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Name required", "Please enter your name.")
            return
        self.name = name
        self.character = "🧑‍🚀" if self.char_var.get() == "Boy" else "👩‍🚀"
        self.score = 0
        self.show_map()

    def show_map(self):
        self.clear()
        self.root.configure(bg="#e7f2fb")
        self.make_header(self.root, f"PLAYER: {self.name.upper()}   •   SCORE: {self.score}")
        body = tk.Frame(self.root, bg="#e7f2fb", padx=30, pady=22)
        body.pack(expand=True, fill="both")
        self.title(body, "CHOOSE YOUR NEXT ROOM", 27).pack(pady=(4, 6))
        tk.Label(body, text=f"{self.character}  Hello {self.name}! Pick a door and begin learning.",
                 font=("Arial", 13), bg="#e7f2fb", fg="#536d86").pack(pady=(0, 18))

        cards = tk.Frame(body, bg="#e7f2fb")
        cards.pack(expand=True)
        descriptions = {
            "IT Basics": "Discover computers and IT",
            "Python": "Try beginner code questions",
            "Networking": "Explore connected devices",
            "Database": "Learn how data is stored",
        }
        for i, room in enumerate(ROOMS):
            r, c = divmod(i, 2)
            color = ROOM_COLORS[room]
            card = tk.Frame(cards, bg="white", padx=18, pady=13,
                            highlightbackground="#c7d9e8", highlightthickness=2)
            card.grid(row=r, column=c, padx=14, pady=11, sticky="nsew")
            tk.Label(card, text=ROOM_ICONS[room], font=("Arial", 31),
                     bg="white").pack()
            tk.Label(card, text=room, font=("Arial", 17, "bold"),
                     bg="white", fg="#203653").pack(pady=4)
            tk.Label(card, text=descriptions[room], font=("Arial", 10),
                     bg="white", fg="#6b7f92").pack(pady=3)
            self.button(card, "OPEN DOOR  ➜", lambda rm=room: self.start_room(rm),
                        color).pack(fill="x", pady=(8, 2))
        self.button(body, "HOME", self.show_welcome, "#71849a").pack(pady=12)

    def start_room(self, room):
        self.room = room
        self.q_index = 0
        self.room_score = 0
        self.show_question()

    def show_question(self):
        self.clear()
        self.answered = False
        question, answers, correct = ROOMS[self.room][self.q_index]
        order = list(range(len(answers)))
        random.shuffle(order)
        self.current_options = [answers[i] for i in order]
        self.correct_display_index = order.index(correct)

        self.root.configure(bg="#f0ebfa")
        self.make_header(self.root, f"{self.room.upper()}  •  SCORE: {self.score}")
        body = tk.Frame(self.root, bg="#f0ebfa", padx=35, pady=25)
        body.pack(expand=True, fill="both")

        self.title(body, f"{ROOM_ICONS[self.room]}  {self.room.upper()} CHALLENGE", 25).pack(pady=5)
        tk.Label(body, text=f"QUESTION {self.q_index + 1} OF {len(ROOMS[self.room])}",
                 font=("Arial", 11, "bold"), bg="#f0ebfa", fg="#75849a").pack(pady=5)

        panel = tk.Frame(body, bg="white", padx=25, pady=22,
                         highlightbackground="#d5c9ea", highlightthickness=2)
        panel.pack(fill="x", pady=20)
        tk.Label(panel, text=f"{self.character}  {self.name}, can you solve this?",
                 font=("Arial", 12, "bold"), bg="white", fg="#7355a0").pack(pady=(0, 12))
        tk.Label(panel, text=question, font=("Arial", 18, "bold"),
                 bg="white", fg="#203653", wraplength=750).pack(pady=8)

        self.feedback = tk.Label(body, text="Choose one answer:",
                                 font=("Arial", 12), bg="#f0ebfa", fg="#687b91")
        self.feedback.pack(pady=5)
        self.answer_buttons = []
        for i, answer in enumerate(self.current_options):
            b = self.button(body, f"{chr(65+i)}     {answer}",
                            lambda idx=i: self.check_answer(idx), "#547fb2")
            b.pack(fill="x", pady=5)
            self.answer_buttons.append(b)

        bottom = tk.Frame(body, bg="#f0ebfa")
        bottom.pack(fill="x", pady=15)
        self.button(bottom, "← ADVENTURE MAP", self.show_map, "#71849a").pack(side="left")
        self.next_btn = self.button(bottom, "NEXT QUESTION  ➜", self.next_question, "#239b68")
        # Hidden until an answer is selected.

    def check_answer(self, selected):
        if self.answered:
            return
        self.answered = True
        for b in self.answer_buttons:
            b.configure(state="disabled")
        if selected == self.correct_display_index:
            self.score += 10
            self.room_score += 10
            self.feedback.config(text="✓ Correct! You earned 10 points.", fg="#16834a")
            self.answer_buttons[selected].configure(bg="#239b68", fg="white")
        else:
            self.feedback.config(text="Not quite! The correct answer is highlighted.", fg="#b74747")
            self.answer_buttons[selected].configure(bg="#c65c5c", fg="white")
            self.answer_buttons[self.correct_display_index].configure(bg="#239b68", fg="white")
        self.next_btn.pack(side="right")

    def next_question(self):
        self.q_index += 1
        if self.q_index < len(ROOMS[self.room]):
            self.show_question()
        else:
            self.show_room_result()

    def show_room_result(self):
        self.clear()
        self.root.configure(bg="#e8f7ee")
        self.make_header(self.root, "ROOM COMPLETED")
        body = tk.Frame(self.root, bg="#e8f7ee")
        body.pack(expand=True, fill="both")
        self.title(body, "✦  WELL DONE!  ✦", 32, "#176b43").pack(pady=(70, 20))
        tk.Label(body, text=f"{self.character}  {self.name}",
                 font=("Arial", 21, "bold"), bg="#e8f7ee", fg="#24466b").pack(pady=8)
        tk.Label(body, text=f"You completed {self.room}!",
                 font=("Arial", 17), bg="#e8f7ee").pack(pady=8)
        tk.Label(body, text=f"+{self.room_score} POINTS",
                 font=("Arial", 25, "bold"), bg="#e8f7ee", fg="#c18a20").pack(pady=15)
        tk.Label(body, text=f"Total score: {self.score}",
                 font=("Arial", 15, "bold"), bg="#e8f7ee", fg="#536d86").pack(pady=5)
        self.button(body, "BACK TO ADVENTURE MAP", self.show_map, "#2878c8").pack(pady=25)
        self.button(body, "FINISH GAME", self.finish, "#239b68").pack()

    def finish(self):
        try:
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL, character TEXT NOT NULL, score INTEGER NOT NULL
            )""")
            cur.execute("INSERT INTO players (name, character, score) VALUES (?, ?, ?)",
                        (self.name, self.character, self.score))
            con.commit()
            con.close()
            saved = "Your result was saved in the database."
        except sqlite3.Error:
            saved = "Game completed. Database save was not successful."

        self.clear()
        self.root.configure(bg="#fff4dc")
        self.make_header(self.root, "ADVENTURE COMPLETE")
        body = tk.Frame(self.root, bg="#fff4dc")
        body.pack(expand=True, fill="both")
        self.title(body, "🏆  YOU ARE A TECH EXPLORER!", 27, "#9a6b16").pack(pady=(65, 25))
        tk.Label(body, text=f"{self.character}  {self.name}",
                 font=("Arial", 21, "bold"), bg="#fff4dc", fg="#24466b").pack(pady=8)
        tk.Label(body, text="You completed your IT adventure!",
                 font=("Arial", 17), bg="#fff4dc").pack(pady=8)
        tk.Label(body, text=f"FINAL SCORE: {self.score} / 200",
                 font=("Arial", 25, "bold"), bg="#fff4dc", fg="#bd831b").pack(pady=20)
        tk.Label(body, text=saved, font=("Arial", 11),
                 bg="#fff4dc", fg="#6b7f92").pack(pady=5)
        self.button(body, "PLAY AGAIN", self.show_welcome, "#239b68").pack(pady=15)
        self.button(body, "EXIT", self.root.destroy, "#71849a").pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = ITAdventure(root)
    root.mainloop()

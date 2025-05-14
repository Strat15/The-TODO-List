"""This is a simple checklist list application that uses tkinter and sqlite3."""

from tkinter import *
from tkinter import messagebox
import sqlite3

con = sqlite3.connect("tododata.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS list (title TEXT, description TEXT)")

res = cur.execute("SELECT title FROM list")
print(res.fetchall())


class TodoApp:
    """This is the main class of the application."""

    def __init__(self, master):
        """This is the constructor of the class."""
        self.master = master
        self.master.title("The TODO List")
        self.master.geometry("800x500")
        self.master.config(bg="black")

        self.rows = cur.execute(
            "SELECT title, description FROM list"
            ).fetchall()

        self.create_widgets()

    def create_widgets(self):
        """This function creates widgets of the application."""
        for row in self.rows:
            frame = Frame(self.master, bg="black")
            frame.pack(anchor=W, padx=20, pady=5)

            tickbox = Checkbutton(frame, text=f"task: {row[0]}, description: {row[1]}", fg="white")
            tickbox.pack(side=LEFT)

            delete_button = Button(frame, command=lambda title=row[0]: self.delete_task(title), bg="red", text="X")
            delete_button.pack(side=LEFT, padx=10)

        self.namebox = Text(self.master, height=2, width=30, bg="black", fg="white")
        self.namebox.pack(pady=20)
        self.namebox.insert(END, "Enter task name here")

        self.descbox = Text(self.master, height=2, width=30, bg="black", fg="white")
        self.descbox.pack(pady=20)
        self.descbox.insert(END, "Enter task description here")

        self.addtaskbutton = Button(self.master, text="Add Task", command=self.add_task, bg="black", fg="white")
        self.addtaskbutton.pack(pady=20)

    def add_task(self):
        """This function adds a task to the database."""
        name = self.namebox.get("1.0", END).strip()
        description = self.descbox.get("1.0", END).strip()
        if name and description:
            cur.execute("INSERT INTO list VALUES(?, ?)", (name, description))
            con.commit()
            messagebox.showinfo("Success", "Task added successfully")
            self.master.destroy()
            mainloop()
        if not name or not description:
            messagebox.showerror("Error", "task name and description cant be empty")
        else:
            messagebox.showerror("Error")

    def delete_task(self, title):
        """This function deletes a task from the database."""
        if title:
            cur.execute("DELETE FROM list WHERE title=?", (title,))
            con.commit()
            messagebox.showinfo("Success", "Task deleted successfully")
            self.master.destroy()
            mainloop()


if __name__ == "__main__":
    root = Tk()
    app = TodoApp(root)
    root.mainloop()

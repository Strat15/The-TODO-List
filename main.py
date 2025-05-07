from tkinter import *
from tkinter import messagebox
import sqlite3

con = sqlite3.connect("./tododata.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS list (title TEXT, priority INTEGER, description TEXT)")

cur.execute("INSERT INTO list VALUES('Buy groceries', 1, 'Buy milk, eggs, and bread')")
cur.execute("INSERT INTO list VALUES('Clean the house', 2, 'Vacuum and dust the living room')")
cur.execute("INSERT INTO list VALUES('Finish homework', 1, 'Complete math and science assignments')")
cur.execute("INSERT INTO list VALUES('Go for a walk', 3, 'Walk in the park for 30 minutes')")

res = cur.execute("SELECT title FROM list")
print(res.fetchall())


class TodoList:
    def __init__(self, name, priority, description):
        self.name = name
        self.priority = priority
        self.description = description

    def add_task(self):
        if self.name and self.priority and self.description:
            cur.execute("INSERT INTO list VALUES(?, ?, ?)", (self.name, self.priority, self.description))
            con.commit()
            messagebox.showinfo("Success", "Task added successfully")
        else:
            messagebox.showerror("Error", "Please fill in all fields")

if __name__ == "__main__":
    root = Tk()
    root.title("The TODO List")
    root.geometry("800x500")
    root.config(bg="black")

    res = cur.execute("SELECT title, description FROM list")
    rows = res.fetchall()        
    for row in rows:
        tickbox = Checkbutton(root, text=f"title: {row[0]}, description: {row[1]}", bg="black", fg="white")
        tickbox.pack(anchor=W, padx=20, pady=5)
    
    namebox = Text(root, height=2, width=30, bg="black", fg="white")
    namebox.pack(pady=20)
    namebox.insert(END, "Enter task name here")
    

    descbox = Text(root, height=2, width=30, bg="black", fg="white")
    descbox.pack(pady=20)
    descbox.insert(END, "Enter task description here")


    addtaskbutton = Button(root, text="Add Task", bg="black", fg="white", command=lambda: TodoList(namebox.get(), 1, descbox.get()).add_task())
    addtaskbutton.pack(pady=20)

    root.mainloop()


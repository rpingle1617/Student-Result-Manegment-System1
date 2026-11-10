from tkinter import *
from tkinter import messagebox
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "rms.db")


class reportClass:

    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1100x480+80+170")
        self.root.config(bg="white")
        self.root.focus_force()

        self.search_id = None   # rid of the result currently shown

        # =============== TITLE ===============
        Label(
            self.root,
            text="View Student Results",
            font=("Calibri", 20, "bold"),
            bg="orange",
            fg="#262626"
        ).place(x=10, y=15, width=1080, height=50)

        # =============== SEARCH ===============
        self.var_search = StringVar()

        Label(
            self.root,
            text="Search By | Roll No.",
            font=("Calibri", 20, "bold"),
            bg="white"
        ).place(x=220, y=100)

        Entry(
            self.root,
            textvariable=self.var_search,
            font=("Calibri", 20),
            bg="lightyellow"
        ).place(x=450, y=100, width=200)

        Button(
            self.root,
            text="Search",
            font=("Calibri", 15, "bold"),
            bg="#03a9f4",
            fg="white",
            cursor="hand2",
            command=self.search
        ).place(x=680, y=100, width=100, height=35)

        Button(
            self.root,
            text="Clear",
            font=("Calibri", 15, "bold"),
            bg="gray",
            fg="white",
            cursor="hand2",
            command=self.clear
        ).place(x=800, y=100, width=100, height=35)

        # =============== TABLE HEADERS ===============
        headers = [
            "Roll No", "Name", "Course",
            "Marks Obtained", "Total Marks", "Percentage"
        ]
        for i, text in enumerate(headers):
            Label(
                self.root,
                text=text,
                font=("Calibri", 15, "bold"),
                bg="white",
                bd=2,
                relief=GROOVE
            ).place(x=150 + i * 130, y=230, width=130, height=50)

        # =============== TABLE VALUES ===============
        self.value_labels = []
        for i in range(6):
            lbl = Label(
                self.root,
                font=("Calibri", 15),
                bg="white",
                bd=2,
                relief=GROOVE
            )
            lbl.place(x=150 + i * 130, y=280, width=130, height=50)
            self.value_labels.append(lbl)

        # =============== DELETE BUTTON ===============
        Button(
            self.root,
            text="Delete",
            font=("Calibri", 15, "bold"),
            bg="red",
            fg="white",
            cursor="hand2",
            command=self.delete
        ).place(x=450, y=350, width=150, height=35)

    # =============== SEARCH ===============
    def search(self):
        roll = self.var_search.get().strip()
        if roll == "":
            messagebox.showerror(
                "Error", "Roll No. is required", parent=self.root
            )
            return

        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        try:
            cur.execute(
                "SELECT rid, roll, name, course, marks_ob, full_marks, per "
                "FROM result WHERE roll=?",
                (roll,)
            )
            row = cur.fetchone()
            if row is not None:
                self.search_id = row[0]
                for lbl, value in zip(self.value_labels, row[1:]):
                    lbl.config(text=value)
            else:
                self.search_id = None
                self.clear_labels()
                messagebox.showerror(
                    "Error", "No record found", parent=self.root
                )
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to {str(ex)}", parent=self.root
            )
        finally:
            con.close()

    # =============== CLEAR ===============
    def clear_labels(self):
        for lbl in self.value_labels:
            lbl.config(text="")

    def clear(self):
        self.search_id = None
        self.var_search.set("")
        self.clear_labels()

    # =============== DELETE ===============
    def delete(self):
        if self.search_id is None:
            messagebox.showerror(
                "Error", "Please search a student result first",
                parent=self.root
            )
            return

        if not messagebox.askyesno(
            "Confirm", "Do you really want to delete this result?",
            parent=self.root
        ):
            return

        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        try:
            cur.execute("DELETE FROM result WHERE rid=?", (self.search_id,))
            con.commit()
            messagebox.showinfo(
                "Delete", "Result deleted successfully", parent=self.root
            )
            self.clear()
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to {str(ex)}", parent=self.root
            )
        finally:
            con.close()


# =============== RUN STANDALONE (for testing) ===============
if __name__ == "__main__":
    root = Tk()
    obj = reportClass(root)
    root.mainloop()
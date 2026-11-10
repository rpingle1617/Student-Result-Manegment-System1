from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "rms.db")


def img_path(name):
    return os.path.join(BASE_DIR, "images", name)


class resultClass:

    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1100x480+80+170")
        self.root.config(bg="white")
        self.root.focus_force()

        # =============== TITLE ===============
        Label(
            self.root,
            text="Add Student Result",
            font=("Calibri", 20, "bold"),
            bg="orange",
            fg="#262626"
        ).place(x=10, y=15, width=1080, height=50)

        # =============== VARIABLES ===============
        self.var_roll = StringVar()
        self.var_name = StringVar()
        self.var_course = StringVar()
        self.var_marks = StringVar()
        self.var_full_marks = StringVar()
        self.roll_list = []

        self.fetch_roll()

        # =============== LABELS ===============
        label_font = ("Calibri", 20, "bold")

        Label(self.root, text="Select Student", font=label_font,
              bg="white").place(x=50, y=100)
        Label(self.root, text="Name", font=label_font,
              bg="white").place(x=50, y=160)
        Label(self.root, text="Course", font=label_font,
              bg="white").place(x=50, y=220)
        Label(self.root, text="Marks Obtained", font=label_font,
              bg="white").place(x=50, y=280)
        Label(self.root, text="Full Marks", font=label_font,
              bg="white").place(x=50, y=340)

        # =============== ENTRY FIELDS ===============
        self.txt_student = ttk.Combobox(
            self.root,
            textvariable=self.var_roll,
            values=self.roll_list,
            font=("Calibri", 15, "bold"),
            state="readonly",
            justify=CENTER
        )
        self.txt_student.place(x=280, y=100, width=200)
        self.txt_student.set("Select")

        Button(
            self.root,
            text="Search",
            font=("Calibri", 15, "bold"),
            bg="#03a9f4",
            fg="white",
            cursor="hand2",
            command=self.search
        ).place(x=500, y=100, width=100, height=28)

        Entry(
            self.root,
            textvariable=self.var_name,
            font=("Calibri", 20, "bold"),
            bg="lightgray",
            readonlybackground="lightgray",
            state="readonly"
        ).place(x=280, y=160, width=320)

        Entry(
            self.root,
            textvariable=self.var_course,
            font=("Calibri", 20, "bold"),
            bg="lightgray",
            readonlybackground="lightgray",
            state="readonly"
        ).place(x=280, y=220, width=320)

        Entry(
            self.root,
            textvariable=self.var_marks,
            font=("Calibri", 20, "bold"),
            bg="lightyellow"
        ).place(x=280, y=280, width=320)

        Entry(
            self.root,
            textvariable=self.var_full_marks,
            font=("Calibri", 20, "bold"),
            bg="lightyellow"
        ).place(x=280, y=340, width=320)

        # =============== BUTTONS ===============
        Button(
            self.root,
            text="Submit",
            font=("Calibri", 15),
            bg="lightgreen",
            activebackground="lightgreen",
            cursor="hand2",
            command=self.add
        ).place(x=300, y=420, width=120, height=35)

        Button(
            self.root,
            text="Clear",
            font=("Calibri", 15),
            bg="lightgray",
            activebackground="lightgray",
            cursor="hand2",
            command=self.clear
        ).place(x=430, y=420, width=120, height=35)

        # =============== IMAGE ===============
        if os.path.exists(img_path("result.jpg")):
            path = img_path("result.jpg")
        elif os.path.exists(img_path("result.png")):
            path = img_path("result.png")
        else:
            path = None

        if path:
            img = Image.open(path).resize((500, 300))
            self.bg_img = ImageTk.PhotoImage(img)
            Label(self.root, image=self.bg_img, bg="white").place(
                x=630, y=100
            )
        else:
            Label(
                self.root,
                text="(images/result.jpg not found)",
                bg="#EAF1FB"
            ).place(x=630, y=100, width=420, height=300)

    # =============== DATABASE HELPERS ===============
    def create_table(self, cur):
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS result(
                rid INTEGER PRIMARY KEY AUTOINCREMENT,
                roll TEXT,
                name TEXT,
                course TEXT,
                marks_ob TEXT,
                full_marks TEXT,
                per TEXT
            )
            """
        )

    # =============== LOAD STUDENT ROLL NUMBERS ===============
    def fetch_roll(self):
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        try:
            cur.execute("SELECT roll FROM student")
            rows = cur.fetchall()
            self.roll_list = [str(row[0]) for row in rows]
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        finally:
            con.close()

    # =============== SEARCH STUDENT ===============
    def search(self):
        if self.var_roll.get() in ("", "Select"):
            messagebox.showerror(
                "Error", "Please select a student roll number",
                parent=self.root
            )
            return

        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        try:
            cur.execute(
                "SELECT name, course FROM student WHERE roll=?",
                (self.var_roll.get(),)
            )
            row = cur.fetchone()
            if row is not None:
                self.var_name.set(row[0])
                self.var_course.set(row[1])
            else:
                messagebox.showerror(
                    "Error", "No record found", parent=self.root
                )
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to {str(ex)}", parent=self.root
            )
        finally:
            con.close()

    # =============== SUBMIT RESULT ===============
    def add(self):
        if self.var_name.get() == "":
            messagebox.showerror(
                "Error", "Please search a student first", parent=self.root
            )
            return

        if self.var_marks.get() == "" or self.var_full_marks.get() == "":
            messagebox.showerror(
                "Error", "Marks fields are required", parent=self.root
            )
            return

        try:
            marks = float(self.var_marks.get())
            full = float(self.var_full_marks.get())
        except ValueError:
            messagebox.showerror(
                "Error", "Marks must be numbers", parent=self.root
            )
            return

        if full <= 0:
            messagebox.showerror(
                "Error", "Full marks must be greater than 0",
                parent=self.root
            )
            return

        if marks < 0 or marks > full:
            messagebox.showerror(
                "Error", "Marks obtained must be between 0 and full marks",
                parent=self.root
            )
            return

        per = round((marks * 100) / full, 2)

        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        try:
            self.create_table(cur)

            cur.execute(
                "SELECT * FROM result WHERE roll=? AND course=?",
                (self.var_roll.get(), self.var_course.get())
            )
            if cur.fetchone() is not None:
                messagebox.showerror(
                    "Error", "Result already present for this student",
                    parent=self.root
                )
                return

            cur.execute(
                "INSERT INTO result(roll, name, course, marks_ob, "
                "full_marks, per) VALUES(?,?,?,?,?,?)",
                (
                    self.var_roll.get(),
                    self.var_name.get(),
                    self.var_course.get(),
                    self.var_marks.get(),
                    self.var_full_marks.get(),
                    str(per)
                )
            )
            con.commit()
            messagebox.showinfo(
                "Success", "Result added successfully", parent=self.root
            )
            self.clear()
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to {str(ex)}", parent=self.root
            )
        finally:
            con.close()

    # =============== CLEAR ===============
    def clear(self):
        self.var_roll.set("Select")
        self.var_name.set("")
        self.var_course.set("")
        self.var_marks.set("")
        self.var_full_marks.set("")


# =============== RUN STANDALONE (for testing) ===============
if __name__ == "__main__":
    root = Tk()
    obj = resultClass(root)
    root.mainloop()
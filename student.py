from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

from db import DB_PATH, create_db


class studentClass:

    def __init__(self, root):

        self.root = root
        self.root.title("Student Result Management System")
        self.root.configure(bg="white")

        # MAXIMIZE WINDOW (works on Windows; falls back on other systems)
        try:
            self.root.state("zoomed")
        except TclError:
            self.root.geometry("1350x700+0+0")
        self.root.focus_force()

        FONT = ("Calibri", 15, "bold")

        # =============== TITLE ===============

        title = Label(
            self.root,
            text="Manage Student Details",
            font=("Calibri", 20, "bold"),
            bg="#0b5a6b",
            fg="white"
        )
        title.place(x=10, y=15, width=720, height=40)

        # =============== VARIABLES ===============

        self.var_roll = StringVar()
        self.var_name = StringVar()
        self.var_email = StringVar()
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_contact = StringVar()
        self.var_course = StringVar()
        self.var_admission = StringVar()
        self.var_state = StringVar()
        self.var_city = StringVar()
        self.var_pin = StringVar()
        self.var_search = StringVar()

        self.course_list = ["Select"]
        self.fetch_course()

        # =============== COLUMN 1 ===============

        Label(self.root, text="Roll No.", font=FONT, bg="white").place(x=10, y=70)
        self.txt_roll = Entry(self.root, textvariable=self.var_roll, font=FONT, bg="lightyellow")
        self.txt_roll.place(x=150, y=70, width=200)

        Label(self.root, text="Name", font=FONT, bg="white").place(x=10, y=110)
        Entry(self.root, textvariable=self.var_name, font=FONT, bg="lightyellow").place(x=150, y=110, width=200)

        Label(self.root, text="Email", font=FONT, bg="white").place(x=10, y=150)
        Entry(self.root, textvariable=self.var_email, font=FONT, bg="lightyellow").place(x=150, y=150, width=200)

        Label(self.root, text="Gender", font=FONT, bg="white").place(x=10, y=190)
        self.txt_gender = ttk.Combobox(
            self.root,
            textvariable=self.var_gender,
            values=("Select Gender", "Male", "Female", "Other"),
            state="readonly",
            justify=CENTER,
            font=FONT
        )
        self.txt_gender.place(x=150, y=190, width=200)
        self.txt_gender.current(0)

        Label(self.root, text="State", font=FONT, bg="white").place(x=10, y=230)
        Entry(self.root, textvariable=self.var_state, font=FONT, bg="lightyellow").place(x=150, y=230, width=100)

        Label(self.root, text="City", font=FONT, bg="white").place(x=270, y=230)
        Entry(self.root, textvariable=self.var_city, font=FONT, bg="lightyellow").place(x=330, y=230, width=100)

        Label(self.root, text="Pin Code", font=FONT, bg="white").place(x=450, y=230)
        Entry(self.root, textvariable=self.var_pin, font=FONT, bg="lightyellow").place(x=560, y=230, width=100)

        # =============== COLUMN 2 ===============

        Label(self.root, text="D.O.B(dd-mm-yyyy)", font=FONT, bg="white").place(x=360, y=70)
        Entry(self.root, textvariable=self.var_dob, font=FONT, bg="lightyellow").place(x=560, y=70, width=170)

        Label(self.root, text="Contact No.", font=FONT, bg="white").place(x=360, y=110)
        Entry(self.root, textvariable=self.var_contact, font=FONT, bg="lightyellow").place(x=560, y=110, width=170)

        Label(self.root, text="Select Course", font=FONT, bg="white").place(x=360, y=150)
        self.txt_course = ttk.Combobox(
            self.root,
            textvariable=self.var_course,
            values=self.course_list,
            state="readonly",
            justify=CENTER,
            font=FONT
        )
        self.txt_course.place(x=560, y=150, width=170)
        self.txt_course.current(0)

        Label(self.root, text="Admission Date", font=FONT, bg="white").place(x=360, y=190)
        Entry(self.root, textvariable=self.var_admission, font=FONT, bg="lightyellow").place(x=560, y=190, width=170)

        # =============== ADDRESS ===============

        Label(self.root, text="Address", font=FONT, bg="white").place(x=10, y=270)
        self.txt_address = Text(self.root, font=FONT, bg="lightyellow")
        self.txt_address.place(x=150, y=270, width=580, height=100)

        # =============== BUTTONS ===============

        Button(
            self.root, text="Save", font=FONT, bg="#2196F3", fg="white",
            cursor="hand2", command=self.add
        ).place(x=150, y=400, width=110, height=40)

        Button(
            self.root, text="Update", font=FONT, bg="#4CAF50", fg="white",
            cursor="hand2", command=self.update
        ).place(x=270, y=400, width=110, height=40)

        Button(
            self.root, text="Delete", font=FONT, bg="#F44336", fg="white",
            cursor="hand2", command=self.delete
        ).place(x=390, y=400, width=110, height=40)

        Button(
            self.root, text="Clear", font=FONT, bg="#607D8B", fg="white",
            cursor="hand2", command=self.clear
        ).place(x=510, y=400, width=110, height=40)

        # =============== SEARCH ===============

        Label(self.root, text="Search | Roll No.", font=FONT, bg="white").place(x=760, y=20)
        Entry(self.root, textvariable=self.var_search, font=FONT, bg="lightyellow").place(x=950, y=20, width=180)
        Button(
            self.root, text="Search", font=FONT, bg="#2196F3", fg="white",
            cursor="hand2", command=self.search
        ).place(x=1150, y=20, width=110, height=30)

        # =============== STUDENT TABLE ===============

        self.C_Frame = Frame(self.root, bd=2, relief=RIDGE)
        self.C_Frame.place(x=760, y=70, width=580, height=430)

        scrolly = Scrollbar(self.C_Frame, orient=VERTICAL, width=20)
        scrollx = Scrollbar(self.C_Frame, orient=HORIZONTAL, width=20)

        self.StudentTable = ttk.Treeview(
            self.C_Frame,
            columns=("roll", "name", "email", "gender", "dob", "contact",
                     "admission", "course", "state", "city", "pin", "address"),
            yscrollcommand=scrolly.set,
            xscrollcommand=scrollx.set
        )

        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.pack(side=BOTTOM, fill=X)
        scrollx.config(command=self.StudentTable.xview)
        scrolly.config(command=self.StudentTable.yview)

        headings = [
            ("roll", "Roll No.", 70), ("name", "Name", 130), ("email", "Email", 170),
            ("gender", "Gender", 80), ("dob", "D.O.B", 100), ("contact", "Contact", 110),
            ("admission", "Admission", 100), ("course", "Course", 110), ("state", "State", 90),
            ("city", "City", 90), ("pin", "Pin", 80), ("address", "Address", 250),
        ]
        for col, text, width in headings:
            self.StudentTable.heading(col, text=text, anchor=W)
            self.StudentTable.column(col, width=width, anchor=W, stretch=NO)
        self.StudentTable["show"] = "headings"

        self.StudentTable.pack(fill=BOTH, expand=1)
        self.StudentTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    # =============== FUNCTIONS ===============

    def fetch_course(self):
        con = sqlite3.connect(database=DB_PATH)
        cur = con.cursor()
        try:
            cur.execute("SELECT name FROM course")
            rows = cur.fetchall()
            self.course_list = ["Select"] + [row[0] for row in rows]
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        finally:
            con.close()

    def values(self):
        return (
            self.var_roll.get(),
            self.var_name.get(),
            self.var_email.get(),
            self.var_gender.get(),
            self.var_dob.get(),
            self.var_contact.get(),
            self.var_admission.get(),
            self.var_course.get(),
            self.var_state.get(),
            self.var_city.get(),
            self.var_pin.get(),
            self.txt_address.get("1.0", END).strip(),
        )

    def add(self):
        con = sqlite3.connect(database=DB_PATH)
        cur = con.cursor()
        try:
            if self.var_roll.get() == "":
                messagebox.showerror("Error", "Roll No. should be required", parent=self.root)
            elif not self.var_roll.get().isdigit():
                messagebox.showerror("Error", "Roll No. must be a number", parent=self.root)
            else:
                cur.execute("SELECT * FROM student WHERE roll=?", (self.var_roll.get(),))
                if cur.fetchone() is not None:
                    messagebox.showerror("Error", "Roll No. already present", parent=self.root)
                else:
                    cur.execute(
                        "INSERT INTO student(roll, name, email, gender, dob, contact, admission, course, state, city, pin, address) "
                        "VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                        self.values()
                    )
                    con.commit()
                    messagebox.showinfo("Success", "Student Added Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def update(self):
        con = sqlite3.connect(database=DB_PATH)
        cur = con.cursor()
        try:
            if self.var_roll.get() == "":
                messagebox.showerror("Error", "Please select a student from the list", parent=self.root)
            else:
                cur.execute("SELECT * FROM student WHERE roll=?", (self.var_roll.get(),))
                if cur.fetchone() is None:
                    messagebox.showerror("Error", "Invalid Roll No.", parent=self.root)
                else:
                    v = self.values()
                    cur.execute(
                        "UPDATE student SET name=?, email=?, gender=?, dob=?, contact=?, admission=?, "
                        "course=?, state=?, city=?, pin=?, address=? WHERE roll=?",
                        v[1:] + (v[0],)
                    )
                    con.commit()
                    messagebox.showinfo("Success", "Student Updated Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def delete(self):
        con = sqlite3.connect(database=DB_PATH)
        cur = con.cursor()
        try:
            if self.var_roll.get() == "":
                messagebox.showerror("Error", "Please select a student from the list", parent=self.root)
            else:
                cur.execute("SELECT * FROM student WHERE roll=?", (self.var_roll.get(),))
                if cur.fetchone() is None:
                    messagebox.showerror("Error", "Invalid Roll No.", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                    if op:
                        cur.execute("DELETE FROM student WHERE roll=?", (self.var_roll.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Student Deleted Successfully", parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def clear(self):
        self.txt_roll.config(state=NORMAL)
        self.var_roll.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.txt_gender.current(0)
        self.var_dob.set("")
        self.var_contact.set("")
        self.var_admission.set("")
        self.txt_course.current(0)
        self.var_state.set("")
        self.var_city.set("")
        self.var_pin.set("")
        self.txt_address.delete("1.0", END)
        self.var_search.set("")
        self.show()

    def show(self):
        con = sqlite3.connect(database=DB_PATH)
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM student")
            rows = cur.fetchall()
            self.StudentTable.delete(*self.StudentTable.get_children())
            for row in rows:
                self.StudentTable.insert("", END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def get_data(self, ev):
        selected = self.StudentTable.focus()
        values = self.StudentTable.item(selected)["values"]
        if not values:
            return
        # read the row again from the database so values like 0123 keep their zeros
        con = sqlite3.connect(database=DB_PATH)
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM student WHERE roll=?", (values[0],))
            row = cur.fetchone()
        finally:
            con.close()
        if row is None:
            return
        self.txt_roll.config(state="readonly")
        self.var_roll.set(row[0])
        self.var_name.set(row[1])
        self.var_email.set(row[2])
        self.var_gender.set(row[3])
        self.var_dob.set(row[4])
        self.var_contact.set(row[5])
        self.var_admission.set(row[6])
        self.var_course.set(row[7])
        self.var_state.set(row[8])
        self.var_city.set(row[9])
        self.var_pin.set(row[10])
        self.txt_address.delete("1.0", END)
        self.txt_address.insert(END, row[11])

    def search(self):
        con = sqlite3.connect(database=DB_PATH)
        cur = con.cursor()
        try:
            if self.var_search.get() == "":
                messagebox.showerror("Error", "Roll No. should be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM student WHERE roll=?", (self.var_search.get(),))
                row = cur.fetchone()
                if row is not None:
                    self.StudentTable.delete(*self.StudentTable.get_children())
                    self.StudentTable.insert("", END, values=row)
                else:
                    messagebox.showerror("Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()


if __name__ == "__main__":
    create_db()
    root = Tk()
    app = studentClass(root)
    root.mainloop()
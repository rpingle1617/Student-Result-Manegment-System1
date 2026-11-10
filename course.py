from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

from db import DB_PATH, create_db


class CourseClass:

    def __init__(self, root):

        self.root = root
        self.root.title("Student Result Management System")
        self.root.configure(bg="#FAFCF8")

        # MAXIMIZE WINDOW (works on Windows; falls back on other systems)
        try:
            self.root.state("zoomed")
        except TclError:
            self.root.geometry("1350x700+0+0")
        self.root.focus_force()

        # =============== TITLE ===============

        title = Label(
            self.root,
            text="Manage Course Detail",
            font=("Calibri", 20, "bold"),
            bg="#033054",
            fg="white"
        )
        title.place(x=0, y=0, relwidth=1, height=50)

        # =============== VARIABLES ===============

        self.var_course = StringVar()
        self.var_duration = StringVar()
        self.var_charges = StringVar()
        self.var_search = StringVar()
        self.var_cid = ""   # id of the row selected in the table

        # =============== COURSE NAME ===============

        lbl_courseName = Label(
            self.root,
            text="Course Name",
            font=("Calibri", 15, "bold"),
            bg="#FAFCF8"
        )
        lbl_courseName.place(x=10, y=70)

        self.text_courseName = Entry(
            self.root,
            textvariable=self.var_course,
            font=("Calibri", 15, "bold"),
            bg="lightyellow"
        )
        self.text_courseName.place(x=150, y=70, width=200)

        # =============== DURATION ===============

        lbl_duration = Label(
            self.root,
            text="Duration",
            font=("Calibri", 15, "bold"),
            bg="#FAFCF8"
        )
        lbl_duration.place(x=10, y=120)

        self.text_duration = Entry(
            self.root,
            textvariable=self.var_duration,
            font=("Calibri", 15, "bold"),
            bg="lightyellow"
        )
        self.text_duration.place(x=150, y=120, width=200)

        # =============== CHARGES ===============

        lbl_charges = Label(
            self.root,
            text="Charges",
            font=("Calibri", 15, "bold"),
            bg="#FAFCF8"
        )
        lbl_charges.place(x=10, y=170)

        self.text_charges = Entry(
            self.root,
            textvariable=self.var_charges,
            font=("Calibri", 15, "bold"),
            bg="lightyellow"
        )
        self.text_charges.place(x=150, y=170, width=200)

        # =============== DESCRIPTION ===============

        lbl_description = Label(
            self.root,
            text="Description",
            font=("Calibri", 15, "bold"),
            bg="#FAFCF8"
        )
        lbl_description.place(x=10, y=220)

        self.text_description = Text(
            self.root,
            font=("Calibri", 15, "bold"),
            bg="lightyellow"
        )
        self.text_description.place(x=150, y=220, width=500, height=100)

        # =============== BUTTONS ===============

        self.btn_add = Button(
            self.root,
            text="Save",
            font=("Calibri", 15, "bold"),
            bg="#2196F3",
            fg="white",
            cursor="hand2",
            command=self.add
        )
        self.btn_add.place(x=150, y=350, width=110, height=40)

        self.btn_update = Button(
            self.root,
            text="Update",
            font=("Calibri", 15, "bold"),
            bg="#4CAF50",
            fg="white",
            cursor="hand2",
            command=self.update
        )
        self.btn_update.place(x=270, y=350, width=110, height=40)

        self.btn_delete = Button(
            self.root,
            text="Delete",
            font=("Calibri", 15, "bold"),
            bg="#F44336",
            fg="white",
            cursor="hand2",
            command=self.delete
        )
        self.btn_delete.place(x=390, y=350, width=110, height=40)

        self.btn_clear = Button(
            self.root,
            text="Clear",
            font=("Calibri", 15, "bold"),
            bg="#607D8B",
            fg="white",
            cursor="hand2",
            command=self.clear
        )
        self.btn_clear.place(x=510, y=350, width=110, height=40)

        # =============== SEARCH COURSE ===============

        lbl_search_courseName = Label(
            self.root,
            text="Course Name",
            font=("Calibri", 15, "bold"),
            bg="#FAFCF8"
        )
        lbl_search_courseName.place(x=700, y=60)

        self.text_search_courseName = Entry(
            self.root,
            textvariable=self.var_search,
            font=("Calibri", 15, "bold"),
            bg="lightyellow"
        )
        self.text_search_courseName.place(x=870, y=60, width=180)

        self.btn_search = Button(
            self.root,
            text="Search",
            font=("Calibri", 15, "bold"),
            bg="#2196F3",
            fg="white",
            cursor="hand2",
            command=self.search
        )
        self.btn_search.place(x=1070, y=60, width=110, height=30)

        # =============== COURSE TABLE FRAME ===============

        self.C_Frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        self.C_Frame.place(x=700, y=110, width=650, height=400)

        scrolly = Scrollbar(self.C_Frame, orient=VERTICAL)
        scrollx = Scrollbar(self.C_Frame, orient=HORIZONTAL)

        self.CourseTable = ttk.Treeview(
            self.C_Frame,
            columns=("cid", "name", "duration", "charges", "description"),
            yscrollcommand=scrolly.set,
            xscrollcommand=scrollx.set
        )

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.CourseTable.xview)
        scrolly.config(command=self.CourseTable.yview)

        # headings and data use the same alignment (W = left) so they line up
        self.CourseTable.heading("cid", text="Course ID", anchor=W)
        self.CourseTable.heading("name", text="Name", anchor=W)
        self.CourseTable.heading("duration", text="Duration", anchor=W)
        self.CourseTable.heading("charges", text="Charges", anchor=W)
        self.CourseTable.heading("description", text="Description", anchor=W)
        self.CourseTable["show"] = "headings"

        self.CourseTable.column("cid", width=80, anchor=W, stretch=NO)
        self.CourseTable.column("name", width=150, anchor=W, stretch=NO)
        self.CourseTable.column("duration", width=100, anchor=W, stretch=NO)
        self.CourseTable.column("charges", width=100, anchor=W, stretch=NO)
        self.CourseTable.column("description", width=400, anchor=W, stretch=NO)

        self.CourseTable.pack(fill=BOTH, expand=1)
        self.CourseTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    # =============== FUNCTIONS ===============

    def add(self):
        con = sqlite3.connect(database=DB_PATH)
        cur = con.cursor()
        try:
            if self.var_course.get() == "":
                messagebox.showerror("Error", "Course Name should be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM course WHERE name=?", (self.var_course.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Course Name already present", parent=self.root)
                else:
                    cur.execute(
                        "INSERT INTO course(name, duration, charges, description) VALUES(?,?,?,?)",
                        (
                            self.var_course.get(),
                            self.var_duration.get(),
                            self.var_charges.get(),
                            self.text_description.get("1.0", END).strip(),
                        )
                    )
                    con.commit()
                    messagebox.showinfo("Success", "Course Added Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def show(self):
        con = sqlite3.connect(database=DB_PATH)
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM course")
            rows = cur.fetchall()
            self.CourseTable.delete(*self.CourseTable.get_children())
            for row in rows:
                self.CourseTable.insert("", END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def get_data(self, ev):
        selected = self.CourseTable.focus()
        values = self.CourseTable.item(selected)["values"]
        if not values:
            return
        self.var_cid = values[0]
        self.var_course.set(values[1])
        self.var_duration.set(values[2])
        self.var_charges.set(values[3])
        self.text_description.delete("1.0", END)
        self.text_description.insert(END, values[4])

    def update(self):
        con = sqlite3.connect(database=DB_PATH)
        cur = con.cursor()
        try:
            if self.var_cid == "":
                messagebox.showerror("Error", "Please select a course from the list", parent=self.root)
            elif self.var_course.get() == "":
                messagebox.showerror("Error", "Course Name should be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM course WHERE name=? AND cid!=?", (self.var_course.get(), self.var_cid))
                if cur.fetchone() is not None:
                    messagebox.showerror("Error", "Course Name already present", parent=self.root)
                else:
                    cur.execute(
                        "UPDATE course SET name=?, duration=?, charges=?, description=? WHERE cid=?",
                        (
                            self.var_course.get(),
                            self.var_duration.get(),
                            self.var_charges.get(),
                            self.text_description.get("1.0", END).strip(),
                            self.var_cid,
                        )
                    )
                    con.commit()
                    messagebox.showinfo("Success", "Course Updated Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def delete(self):
        con = sqlite3.connect(database=DB_PATH)
        cur = con.cursor()
        try:
            if self.var_cid == "":
                messagebox.showerror("Error", "Please select a course from the list", parent=self.root)
            else:
                op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                if op:
                    cur.execute("DELETE FROM course WHERE cid=?", (self.var_cid,))
                    con.commit()
                    messagebox.showinfo("Delete", "Course Deleted Successfully", parent=self.root)
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def clear(self):
        self.var_cid = ""
        self.var_course.set("")
        self.var_duration.set("")
        self.var_charges.set("")
        self.var_search.set("")
        self.text_description.delete("1.0", END)
        self.show()

    def search(self):
        con = sqlite3.connect(database=DB_PATH)
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM course WHERE name LIKE ?", ("%" + self.var_search.get() + "%",))
            rows = cur.fetchall()
            self.CourseTable.delete(*self.CourseTable.get_children())
            if rows:
                for row in rows:
                    self.CourseTable.insert("", END, values=row)
            else:
                messagebox.showerror("Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()


if __name__ == "__main__":
    create_db()
    root = Tk()
    app = CourseClass(root)
    root.mainloop()
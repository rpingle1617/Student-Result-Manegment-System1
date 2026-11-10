from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
import hashlib
import re
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "rms.db")


def img_path(name):
    return os.path.join(BASE_DIR, "images", name)


def hash_password(password):
    """Never store plain-text passwords. Use the same function in login."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


class Register:

    # ---- colours / fonts (matched to the design) ----
    BLUE = "#0B2A5B"
    GREEN_TEXT = "#0A6B14"
    GREEN_BTN = "#2F9E4F"
    FIELD_BG = "#D6D6D6"
    LABEL_FG = "#7A7A7A"
    LABEL_FONT = ("Calibri", 12, "bold")
    ENTRY_FONT = ("Calibri", 12)

    def __init__(self, root):
        self.root = root
        self.root.title("Registration Window")
        self.root.geometry("1000x470+250+120")
        self.root.config(bg="white")
        self.root.resizable(False, False)

        # =============== VARIABLES ===============
        self.var_fname = StringVar()
        self.var_lname = StringVar()
        self.var_contact = StringVar()
        self.var_email = StringVar()
        self.var_question = StringVar()
        self.var_answer = StringVar()
        self.var_password = StringVar()
        self.var_cpassword = StringVar()
        self.var_chk = IntVar()

        self.create_table()

        # =============== LEFT PANEL ===============
        left = Frame(self.root, bg=self.BLUE)
        left.place(x=0, y=0, width=360, height=470)

        if os.path.exists(img_path("side.png")):
            img = Image.open(img_path("side.png")).resize((360, 470))
            self.left_img = ImageTk.PhotoImage(img)
            Label(left, image=self.left_img, bd=0).place(x=0, y=0)

        Label(
            left,
           
            font=("Calibri", 22, "bold"),
            bg=self.BLUE,
            fg="white"
        ).place(relx=0.5, y=150, anchor="center")

        Label(
            left,
           
            font=("Calibri", 11),
            bg=self.BLUE,
            fg="white",
            justify=CENTER
        ).place(relx=0.5, y=240, anchor="center")

        Button(
            left,
            text="Sign In",
            font=("Calibri", 16),
            bg="white",
            fg="#222222",
            activebackground="white",
            bd=0,
            cursor="hand2",
            command=self.login_window
        ).place(relx=0.5, y=350, anchor="center", width=165, height=45)

        # =============== RIGHT FORM ===============
        Label(
            self.root,
            text="REGISTER HERE",
            font=("Calibri", 20, "bold"),
            bg="white",
            fg=self.GREEN_TEXT
        ).place(x=405, y=30)

        col1, col2, w = 405, 690, 225

        # Row 1
        self.field("First Name", self.var_fname, col1, 95, w)
        self.field("Last Name", self.var_lname, col2, 95, w)

        # Row 2
        self.field("Contact No.", self.var_contact, col1, 160, w)
        self.field("Email", self.var_email, col2, 160, w)

        # Row 3
        Label(self.root, text="Security  Question", font=self.LABEL_FONT,
              bg="white", fg=self.LABEL_FG).place(x=col1, y=225)
        self.cmb_quest = ttk.Combobox(
            self.root,
            textvariable=self.var_question,
            values=(
                "Select",
                "Your First Pet Name",
                "Your Birth Place",
                "Your Best Friend Name"
            ),
            state="readonly",
            justify=CENTER,
            font=("Calibri", 11, "bold")
        )
        self.cmb_quest.place(x=col1, y=250, width=w, height=24)
        self.cmb_quest.current(0)

        self.field("Answer", self.var_answer, col2, 225, w)

        # Row 4
        self.field("Password", self.var_password, col1, 290, w, show="*")
        self.field("Confirm Password", self.var_cpassword, col2, 290, w,
                   show="*")

        # Terms
        Checkbutton(
            self.root,
            text="I Agree The Terms & Conditions",
            variable=self.var_chk,
            onvalue=1,
            offvalue=0,
            bg="white",
            activebackground="white",
            font=("Calibri", 11)
        ).place(x=col1 - 3, y=355)

        # Register button
        Button(
            self.root,
            text="REGISTER NOW  \u2192",
            font=("Calibri", 10, "bold"),
            bg=self.GREEN_BTN,
            fg="white",
            activebackground=self.GREEN_BTN,
            activeforeground="white",
            bd=0,
            cursor="hand2",
            command=self.register_data
        ).place(x=col1, y=395, width=w, height=36)

    # =============== HELPER: label + grey entry ===============
    def field(self, text, var, x, y, width, show=""):
        Label(self.root, text=text, font=self.LABEL_FONT,
              bg="white", fg=self.LABEL_FG).place(x=x, y=y)
        Entry(
            self.root,
            textvariable=var,
            font=self.ENTRY_FONT,
            bg=self.FIELD_BG,
            bd=0,
            relief=FLAT,
            show=show
        ).place(x=x, y=y + 25, width=width, height=24)

    # =============== CREATE TABLE ===============
    def create_table(self):
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS employee(
                eid INTEGER PRIMARY KEY AUTOINCREMENT,
                f_name TEXT,
                l_name TEXT,
                contact TEXT,
                email TEXT UNIQUE,
                question TEXT,
                answer TEXT,
                password TEXT
            )
            """
        )
        con.commit()
        con.close()

    # =============== CLEAR FIELDS ===============
    def clear(self):
        self.var_fname.set("")
        self.var_lname.set("")
        self.var_contact.set("")
        self.var_email.set("")
        self.var_answer.set("")
        self.var_password.set("")
        self.var_cpassword.set("")
        self.cmb_quest.current(0)
        self.var_chk.set(0)

    # =============== REGISTER ===============
    def register_data(self):
        fname = self.var_fname.get().strip()
        contact = self.var_contact.get().strip()
        email = self.var_email.get().strip()

        if (
            fname == ""
            or contact == ""
            or email == ""
            or self.var_question.get() == "Select"
            or self.var_answer.get().strip() == ""
            or self.var_password.get() == ""
            or self.var_cpassword.get() == ""
        ):
            messagebox.showerror(
                "Error", "All fields are required", parent=self.root
            )
            return

        if not contact.isdigit() or len(contact) < 10:
            messagebox.showerror(
                "Error", "Enter a valid contact number (at least 10 digits)",
                parent=self.root
            )
            return

        if not re.match(r"^[\w.+-]+@[\w-]+\.[\w.-]+$", email):
            messagebox.showerror(
                "Error", "Enter a valid email address", parent=self.root
            )
            return

        if len(self.var_password.get()) < 6:
            messagebox.showerror(
                "Error", "Password must be at least 6 characters",
                parent=self.root
            )
            return

        if self.var_password.get() != self.var_cpassword.get():
            messagebox.showerror(
                "Error", "Password and Confirm Password must be the same",
                parent=self.root
            )
            return

        if self.var_chk.get() == 0:
            messagebox.showerror(
                "Error", "Please agree to our terms & conditions",
                parent=self.root
            )
            return

        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM employee WHERE email=?", (email,))
            if cur.fetchone() is not None:
                messagebox.showerror(
                    "Error", "User already exists, try another email",
                    parent=self.root
                )
                return

            cur.execute(
                "INSERT INTO employee(f_name, l_name, contact, email, "
                "question, answer, password) VALUES(?,?,?,?,?,?,?)",
                (
                    fname,
                    self.var_lname.get().strip(),
                    contact,
                    email,
                    self.var_question.get(),
                    self.var_answer.get().strip(),
                    hash_password(self.var_password.get())
                )
            )
            con.commit()
            messagebox.showinfo(
                "Success", "Registered successfully", parent=self.root
            )
            self.clear()
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to {str(ex)}", parent=self.root
            )
        finally:
            con.close()

    # =============== SIGN IN ===============
    def login_window(self):
        # Close this window. If you have a login.py, open it here, e.g.:
        #   from login import Login_Window
        #   self.root.destroy()
        #   new_root = Tk(); Login_Window(new_root); new_root.mainloop()
        self.root.destroy()


# =============== RUN APPLICATION ===============
if __name__ == "__main__":
    root = Tk()
    obj = Register(root)
    root.mainloop()
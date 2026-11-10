from tkinter import *
from tkinter import ttk, messagebox, TclError
import sqlite3
import math
import os
import time

from register import Register, hash_password

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "rms.db")


class Login_Window:

    BLUE = "#0A8BCB"
    NAVY = "#061B33"
    CLOCK_BG = "#08141F"
    CRIMSON = "#B5174F"
    FIELD_BG = "#D6D6D6"
    LABEL_FG = "#7A7A7A"
    LABEL_FONT = ("Calibri", 14, "bold")

    def __init__(self, root):
        self.root = root
        self.root.title("Login System")
        self.root.geometry("900x460+250+120")
        self.root.config(bg=self.BLUE)
        self.root.resizable(False, False)

        self.var_email = StringVar()
        self.var_password = StringVar()
        self.after_id = None
        self.success = False   # becomes True after a correct login

        self.create_table()

        # =============== BACKGROUND SHAPES ===============
        Frame(self.root, bg=self.NAVY).place(x=485, y=0, width=415, height=460)
        Frame(self.root, bg="white").place(x=170, y=10, width=730, height=440)

        # =============== CLOCK PANEL ===============
        self.canvas = Canvas(
            self.root,
            width=315,
            height=405,
            bg=self.CLOCK_BG,
            highlightthickness=0
        )
        self.canvas.place(x=30, y=26)

        self.cx, self.cy, self.radius = 157, 235, 105
        self.draw_clock_face()
        self.tick()

        # =============== LOGIN FORM ===============
        Label(
            self.root,
            text="LOGIN HERE",
            font=("Calibri", 26, "bold"),
            bg="white",
            fg=self.BLUE
        ).place(x=400, y=45)

        Label(self.root, text="EMAIL ADDRESS", font=self.LABEL_FONT,
              bg="white", fg=self.LABEL_FG).place(x=400, y=140)
        self.txt_email = Entry(
            self.root,
            textvariable=self.var_email,
            font=("Calibri", 14),
            bg=self.FIELD_BG,
            bd=0,
            relief=FLAT
        )
        self.txt_email.place(x=400, y=170, width=345, height=30)

        Label(self.root, text="PASSWORD", font=self.LABEL_FONT,
              bg="white", fg=self.LABEL_FG).place(x=400, y=225)
        self.txt_pass = Entry(
            self.root,
            textvariable=self.var_password,
            font=("Calibri", 14),
            bg=self.FIELD_BG,
            bd=0,
            relief=FLAT,
            show="*"
        )
        self.txt_pass.place(x=400, y=255, width=345, height=30)

        Button(
            self.root,
            text="Register new Account?",
            font=("Calibri", 11),
            bg="white",
            fg="#8B1538",
            activebackground="white",
            activeforeground="#8B1538",
            bd=0,
            cursor="hand2",
            command=self.register_window
        ).place(x=398, y=295)

        Button(
            self.root,
            text="Forget Password?",
            font=("Calibri", 11),
            bg="white",
            fg="#8B1538",
            activebackground="white",
            activeforeground="#8B1538",
            bd=0,
            cursor="hand2",
            command=self.forget_password_window
        ).place(x=575, y=295)

        Button(
            self.root,
            text="Login",
            font=("Calibri", 15, "bold"),
            bg=self.CRIMSON,
            fg="white",
            activebackground=self.CRIMSON,
            activeforeground="white",
            bd=2,
            relief=RIDGE,
            cursor="hand2",
            command=self.login
        ).place(x=400, y=340, width=125, height=36)

        self.root.bind("<Return>", lambda event: self.login())
        self.txt_email.focus_set()

    # =============== CLOCK ===============
    def draw_clock_face(self):
        c, cx, cy, r = self.canvas, self.cx, self.cy, self.radius

        c.create_text(
            157, 30,
            text="WebCode Clock",
            font=("Calibri", 18, "bold"),
            fill="white"
        )

        # soft outer ring
        c.create_oval(cx - r - 12, cy - r - 12, cx + r + 12, cy + r + 12,
                      outline="#111F2B", width=14)
        c.create_oval(cx - r, cy - r, cx + r, cy + r,
                      fill="#0A1824", outline="#0F1D29", width=2)

        # tick marks
        for i in range(12):
            a = math.radians(i * 30)
            x1 = cx + (r - 18) * math.sin(a)
            y1 = cy - (r - 18) * math.cos(a)
            x2 = cx + (r - 8) * math.sin(a)
            y2 = cy - (r - 8) * math.cos(a)
            c.create_line(x1, y1, x2, y2, fill="#3A4A58", width=2)

        # 12, 3, 6, 9
        for label, angle in ((12, 0), (3, 90), (6, 180), (9, 270)):
            a = math.radians(angle)
            x = cx + (r - 35) * math.sin(a)
            y = cy - (r - 35) * math.cos(a)
            c.create_text(x, y, text=str(label),
                          font=("Calibri", 13, "bold"),
                          fill="#5B6B79")

    def hand(self, length, angle_deg, color, width):
        a = math.radians(angle_deg)
        x = self.cx + length * math.sin(a)
        y = self.cy - length * math.cos(a)
        self.canvas.create_line(
            self.cx, self.cy, x, y,
            fill=color, width=width, capstyle=ROUND, tags="hand"
        )

    def tick(self):
        now = time.localtime()
        h, m, s = now.tm_hour % 12, now.tm_min, now.tm_sec

        self.canvas.delete("hand")
        self.hand(50, h * 30 + m * 0.5, self.CRIMSON, 5)   # hour
        self.hand(80, m * 6 + s * 0.1, "white", 3)          # minute
        self.hand(92, s * 6, "#F5E642", 2)                  # second
        self.canvas.create_oval(
            self.cx - 6, self.cy - 6, self.cx + 6, self.cy + 6,
            fill="#10B5C9", outline="", tags="hand"
        )

        self.after_id = self.root.after(1000, self.tick)

    def stop_clock(self):
        if self.after_id is not None:
            try:
                self.root.after_cancel(self.after_id)
            except TclError:
                pass
            self.after_id = None

    # =============== DATABASE ===============
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

    # =============== LOGIN ===============
    def login(self):
        email = self.var_email.get().strip()
        password = self.var_password.get()

        if email == "" or password == "":
            messagebox.showerror(
                "Error", "All fields are required", parent=self.root
            )
            return

        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        try:
            cur.execute(
                "SELECT eid FROM employee WHERE email=? AND password=?",
                (email, hash_password(password))
            )
            row = cur.fetchone()
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to {str(ex)}", parent=self.root
            )
            return
        finally:
            con.close()

        if row is None:
            messagebox.showerror(
                "Error", "Invalid email or password", parent=self.root
            )
            return

        messagebox.showinfo(
            "Welcome", f"Welcome {email}", parent=self.root
        )
        # Close the login window; main.py then opens the dashboard
        self.success = True
        self.stop_clock()
        self.root.destroy()

    # =============== REGISTER ===============
    def register_window(self):
        win = Toplevel(self.root)
        Register(win)

    # =============== FORGET PASSWORD ===============
    def forget_password_window(self):
        win = Toplevel(self.root)
        win.title("Reset Password")
        win.geometry("400x420+450+200")
        win.config(bg="white")
        win.resizable(False, False)
        win.focus_force()
        win.grab_set()

        var_email = StringVar(value=self.var_email.get())
        var_question = StringVar()
        var_answer = StringVar()
        var_new = StringVar()

        Label(win, text="Reset Password",
              font=("Calibri", 20, "bold"),
              bg="white", fg=self.BLUE).place(x=0, y=20, relwidth=1)

        lbl_font = ("Calibri", 12, "bold")
        ent_font = ("Calibri", 13)

        Label(win, text="Email", font=lbl_font, bg="white",
              fg=self.LABEL_FG).place(x=50, y=75)
        Entry(win, textvariable=var_email, font=ent_font,
              bg=self.FIELD_BG, bd=0).place(x=50, y=100, width=300, height=28)

        Label(win, text="Security Question", font=lbl_font, bg="white",
              fg=self.LABEL_FG).place(x=50, y=140)
        cmb = ttk.Combobox(
            win,
            textvariable=var_question,
            values=(
                "Select",
                "Your First Pet Name",
                "Your Birth Place",
                "Your Best Friend Name"
            ),
            state="readonly",
            justify=CENTER,
            font=("Calibri", 12)
        )
        cmb.place(x=50, y=165, width=300, height=28)
        cmb.current(0)

        Label(win, text="Answer", font=lbl_font, bg="white",
              fg=self.LABEL_FG).place(x=50, y=205)
        Entry(win, textvariable=var_answer, font=ent_font,
              bg=self.FIELD_BG, bd=0).place(x=50, y=230, width=300, height=28)

        Label(win, text="New Password", font=lbl_font, bg="white",
              fg=self.LABEL_FG).place(x=50, y=270)
        Entry(win, textvariable=var_new, font=ent_font, bg=self.FIELD_BG,
              bd=0, show="*").place(x=50, y=295, width=300, height=28)

        def reset():
            email = var_email.get().strip()

            if (
                email == ""
                or var_question.get() == "Select"
                or var_answer.get().strip() == ""
                or var_new.get() == ""
            ):
                messagebox.showerror(
                    "Error", "All fields are required", parent=win
                )
                return

            if len(var_new.get()) < 6:
                messagebox.showerror(
                    "Error", "Password must be at least 6 characters",
                    parent=win
                )
                return

            con = sqlite3.connect(DB_PATH)
            cur = con.cursor()
            try:
                cur.execute(
                    "SELECT eid FROM employee "
                    "WHERE email=? AND question=? AND answer=?",
                    (email, var_question.get(), var_answer.get().strip())
                )
                if cur.fetchone() is None:
                    messagebox.showerror(
                        "Error",
                        "Email, security question or answer is incorrect",
                        parent=win
                    )
                    return

                cur.execute(
                    "UPDATE employee SET password=? WHERE email=?",
                    (hash_password(var_new.get()), email)
                )
                con.commit()
                messagebox.showinfo(
                    "Success", "Password reset successfully", parent=win
                )
                win.destroy()
            except Exception as ex:
                messagebox.showerror(
                    "Error", f"Error due to {str(ex)}", parent=win
                )
            finally:
                con.close()

        Button(
            win,
            text="Reset Password",
            font=("Calibri", 14, "bold"),
            bg=self.CRIMSON,
            fg="white",
            activebackground=self.CRIMSON,
            activeforeground="white",
            bd=0,
            cursor="hand2",
            command=reset
        ).place(x=50, y=350, width=300, height=38)


# =============== RUN APPLICATION ===============
if __name__ == "__main__":
    from sclone import run
    run()
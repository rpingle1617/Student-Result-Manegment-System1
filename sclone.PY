from tkinter import *
from tkinter import TclError, messagebox
from PIL import Image, ImageTk, ImageOps
import os
import sys
import sqlite3

from course import CourseClass
from student import studentClass
from result import resultClass
from report import reportClass
from db import create_db
from login import Login_Window

# Folder where this file is saved (so images load from any run location)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "rms.db")


def img_path(name):
    return os.path.join(BASE_DIR, "images", name)


def make_screen_sharp():
    """Stop Windows from stretching (blurring) the app on high-DPI screens.
    Must be called BEFORE the first Tk() window is created."""
    if sys.platform.startswith("win"):
        import ctypes
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            try:
                ctypes.windll.user32.SetProcessDPIAware()
            except Exception:
                pass


def new_window():
    """Create a main window with the layout size the pages were designed for."""
    window = Tk()
    window.tk.call("tk", "scaling", 96 / 72)   # keeps fonts/layout as designed
    return window


class StudentResultManagement:

    def __init__(self, root):

        self.root = root
        self.logged_out = False   # True only when Logout is pressed
        self.root.title("Student Result Management System")
        self.root.configure(bg="#FAFCF8")

        # Full screen (works on Windows and Linux)
        try:
            self.root.state("zoomed")
        except TclError:
            self.root.attributes("-zoomed", True)

        # =============== HEADER ===============
        title_frame = Frame(self.root, bg="#033054", height=80)
        title_frame.pack(fill=X)
        title_frame.pack_propagate(False)

        header_inner = Frame(title_frame, bg="#033054")
        header_inner.place(relx=0.5, rely=0.5, anchor=CENTER)

        if os.path.exists(img_path("logo_p.png")):
            img = Image.open(img_path("logo_p.png")).resize((50, 50))
            self.logo = ImageTk.PhotoImage(img)
            Label(header_inner, image=self.logo, bg="#033054").pack(
                side=LEFT, padx=(0, 10)
            )

        Label(
            header_inner,
            text="Student Result Management System",
            font=("Calibri", 24, "bold"),
            bg="#033054",
            fg="white"
        ).pack(side=LEFT)

        # =============== MENU ===============
        menu = LabelFrame(
            self.root,
            text="Menus",
            font=("Calibri", 15),
            bg="white"
        )
        menu.pack(fill=X, padx=10, pady=10)

        buttons = [
            "Course",
            "Student",
            "Result",
            "View Student Results",
            "Logout",
            "Exit"
        ]

        commands = {
            "Course": self.add_course,
            "Student": self.add_student,
            "Result": self.add_result,
            "View Student Results": self.view_result,
            "Logout": self.logout,
            "Exit": self.root.destroy
        }

        for i, name in enumerate(buttons):
            menu.grid_columnconfigure(i, weight=1)

            Button(
                menu,
                text=name,
                font=("Calibri", 14, "bold"),
                bg="#0B5377",
                fg="white",
                activebackground="#0B5377",
                activeforeground="white",
                bd=3,
                relief=RIDGE,
                cursor="hand2",
                command=commands.get(name)
            ).grid(row=0, column=i, padx=7, pady=10, sticky="ew")

        # =============== FOOTER ===============
        footer = Frame(self.root, bg="#222222", height=50)
        footer.pack(side=BOTTOM, fill=X)
        footer.pack_propagate(False)

        Label(
            footer,
            text="SRMS - Student Result Management System\n"
                 "Contact Us for any Technical Issue: 987xxxxx01",
            font=("Calibri", 10),
            bg="#222222",
            fg="white",
            justify=CENTER
        ).pack(expand=True, fill=BOTH)

        # =============== DASHBOARD ===============
        dashboard = Frame(self.root, bg="#FAFCF8")
        dashboard.pack(fill=BOTH, expand=True)

        content = Frame(dashboard, bg="#FAFCF8")
        content.place(relx=0.98, rely=0.50, anchor="e")

        self.root.update_idletasks()
        img_w = int(self.root.winfo_screenwidth() * 0.60)
        img_h = int(self.root.winfo_screenheight() * 0.52)

        if os.path.exists(img_path("bg.png")):
            bg = Image.open(img_path("bg.png"))
            bg = ImageOps.contain(bg, (img_w, img_h))
            self.bg_image = ImageTk.PhotoImage(bg)
            Label(content, image=self.bg_image, bg="#FAFCF8").pack(side=TOP)
        else:
            Label(
                content,
                text="(images/bg.png not found)",
                bg="#EAF1FB"
            ).pack(side=TOP, ipadx=img_w // 12, ipady=img_h // 12)

        # ---- Cards row ----
        cards = Frame(content, bg="#FAFCF8")
        cards.pack(side=TOP, fill=X, pady=(5, 0))

        for i in range(3):
            cards.grid_columnconfigure(i, weight=1, uniform="cards")

        self.lbl_course = self.make_card(cards, "Total Courses\n[ 0 ]", "#E43B06")
        self.lbl_course.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        self.lbl_student = self.make_card(cards, "Total Students\n[ 0 ]", "#0676AD")
        self.lbl_student.grid(row=0, column=1, sticky="nsew", padx=5)

        self.lbl_result = self.make_card(cards, "Total Results\n[ 0 ]", "#038074")
        self.lbl_result.grid(row=0, column=2, sticky="nsew", padx=(5, 0))

        # Load the counts from the database (and keep refreshing them)
        self.update_details()

    # =============== LIVE COUNTS FROM DATABASE ===============
    def count_rows(self, cur, table):
        try:
            cur.execute(f"SELECT COUNT(*) FROM {table}")
            return cur.fetchone()[0]
        except sqlite3.Error:
            # table does not exist yet
            return 0

    def update_details(self):
        con = sqlite3.connect(DB_PATH)
        try:
            cur = con.cursor()
            courses = self.count_rows(cur, "course")
            students = self.count_rows(cur, "student")
            results = self.count_rows(cur, "result")
        finally:
            con.close()

        self.lbl_course.config(text=f"Total Courses\n[{courses}]")
        self.lbl_student.config(text=f"Total Students\n[{students}]")
        self.lbl_result.config(text=f"Total Results\n[{results}]")

        # Refresh every 1 second so new records show up automatically
        self.root.after(1000, self.update_details)

    # =============== DASHBOARD CARD ===============
    def make_card(self, parent, text, color):
        return Label(
            parent,
            text=text,
            font=("Calibri", 18),
            bg=color,
            fg="white",
            bd=10,
            relief=RIDGE,
            height=2
        )

    # =============== OPEN COURSE WINDOW ===============
    def add_course(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = CourseClass(self.new_win)

    # =============== OPEN STUDENT WINDOW ===============
    def add_student(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = studentClass(self.new_win)

    # =============== RESULT WINDOW ===============
    def add_result(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = resultClass(self.new_win)

    # =============== VIEW STUDENT RESULT ===============
    def view_result(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = reportClass(self.new_win)

    # =============== LOGOUT ===============
    def logout(self):
        answer = messagebox.askyesno(
            "Logout",
            "Do you want to logout?"
        )

        if answer:
            self.logged_out = True
            self.root.destroy()


# =============== RUN APPLICATION ===============
def run():
    """Create tables -> login -> dashboard -> (logout) -> login again."""
    make_screen_sharp()   # crisp text, no blur
    create_db()           # make sure rms.db and all tables exist

    while True:
        # ---------- 1. LOGIN WINDOW ----------
        root = new_window()
        login = Login_Window(root)
        root.mainloop()

        # Login window closed without a successful login -> quit app
        if not login.success:
            break

        # ---------- 2. DASHBOARD ----------
        root = new_window()
        app = StudentResultManagement(root)
        root.mainloop()

        # Only the Logout button sends the user back to the login page
        if not app.logged_out:
            break


# Always start from the login page
if __name__ == "__main__":
    run()
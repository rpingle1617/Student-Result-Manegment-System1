import sqlite3
import os

# One database file, always next to the code (works from any run location)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "rms.db")


def create_db():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    # 1. Courses  (course.py, dashboard card)
    cur.execute(
        "CREATE TABLE IF NOT EXISTS course("
        "cid INTEGER PRIMARY KEY AUTOINCREMENT, "
        "name TEXT, duration TEXT, charges TEXT, description TEXT)"
    )

    # 2. Students  (student.py, result.py, dashboard card)
    cur.execute(
        "CREATE TABLE IF NOT EXISTS student("
        "roll INTEGER PRIMARY KEY, name TEXT, email TEXT, gender TEXT, "
        "dob TEXT, contact TEXT, admission TEXT, course TEXT, state TEXT, "
        "city TEXT, pin TEXT, address TEXT)"
    )

    # 3. Results  (result.py, report.py, dashboard card)
    cur.execute(
        "CREATE TABLE IF NOT EXISTS result("
        "rid INTEGER PRIMARY KEY AUTOINCREMENT, "
        "roll TEXT, name TEXT, course TEXT, marks_ob TEXT, "
        "full_marks TEXT, per TEXT)"
    )

    # 4. Users who can log in  (register.py, login.py)
    cur.execute(
        "CREATE TABLE IF NOT EXISTS employee("
        "eid INTEGER PRIMARY KEY AUTOINCREMENT, "
        "f_name TEXT, l_name TEXT, contact TEXT, email TEXT UNIQUE, "
        "question TEXT, answer TEXT, password TEXT)"
    )

    con.commit()
    con.close()


if __name__ == "__main__":
    create_db()
    print("Database ready:", DB_PATH)
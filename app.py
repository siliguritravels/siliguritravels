from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# -------- INIT DB ----------
def init_db():
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()

    # contact table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS contact (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT,
        message TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

def init_db():
    conn = sqlite3.connect("travel.db")
    cur = conn.cursor()

    # contact table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        place TEXT,
        date TEXT,
        phone TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()
# -------- HOME ----------
@app.route("/")
def home():
    return render_template("index.html")

# -------- CONTACT SUBMIT ----------
@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    message = request.form.get("message")

    conn = sqlite3.connect("data.db")
    cur = conn.cursor()

    cur.execute("INSERT INTO contact (name, email, phone, message) VALUES (?, ?, ?, ?)",
                (name, email, phone, message))

    conn.commit()
    conn.close()

    return redirect("/")

# -------- ADMIN LOGIN ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "1234":
            session["admin"] = True
            return redirect(url_for("view"))
        else:
            return "Wrong Login ❌"

    return render_template("login.html")

# -------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("home"))

# -------- VIEW (BOOKING + CONTACT BOTH) ----------
@app.route("/view")
def view():
    if not session.get("admin"):
        return redirect(url_for("login"))

    # 🔵 booking DB
    conn1 = sqlite3.connect("travel.db")
    c1 = conn1.cursor()
    c1.execute("SELECT * FROM bookings")
    bookings = c1.fetchall()
    conn1.close()

    # 🟢 contact DB
    conn2 = sqlite3.connect("data.db")
    c2 = conn2.cursor()
    c2.execute("SELECT * FROM contact")
    contacts = c2.fetchall()
    conn2.close()

    return render_template("view.html", bookings=bookings, contacts=contacts)

# -------- BOOKING ----------
@app.route("/book", methods=["POST"])
def book():
    place = request.form["place"]
    date = request.form["date"]
    phone = request.form["phone"]

    conn = sqlite3.connect("travel.db")
    c = conn.cursor()
    c.execute("INSERT INTO bookings (place, date, phone) VALUES (?, ?, ?)", (place, date, phone))
    conn.commit()
    conn.close()

    return "Booking Saved ✅...we will contact you very soon. thank you"

# -------- RUN ----------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
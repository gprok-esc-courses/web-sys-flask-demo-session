import sqlite3
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = 'weljknwejohwerowerhnweornweorhweorhweroiwehreowh'
app.config['SESSION_TYPE'] = 'filesystem'

conn = sqlite3.connect("database.db")
conn.execute("""
             CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             username TEXT,
             password TEXT, 
             role TEXT)
             """)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = sqlite3.connect("database.db")
        user = db.execute("SELECT * FROM users WHERE username=? AND password=?", 
                          (username, password)).fetchone()
        if user is None:
            return render_template("login.html", error="Wrong credentials")
        else:
            session.clear()
            session['username'] = username 
            session['role'] = user[3]
            return redirect("/dashboard")
    return render_template("login.html", error="")

@app.route("/dashboard")
def dashboard():
    if session.get('username') is None:
        return redirect('/login') 
    db = sqlite3.connect('database.db')
    user = db.execute("SELECT * FROM users WHERE username=?", 
                          (session.get('username'),)).fetchone()
    return render_template("dashboard.html", username=user[1], role=user[3])

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
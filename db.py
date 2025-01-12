import sqlite3
from flask import g
from flask import Flask

app = Flask(__name__)

DATABASE = "database.db"

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def selectUserDataById(id):
    with app.app_context():
        cur = get_db().cursor()
        cur.execute("SELECT * FROM users WHERE ID = ?", (id,))
        data = cur.fetchone()
        return data
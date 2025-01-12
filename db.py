import json
import sqlite3
from flask import g
from flask import Flask

app = Flask(__name__)

## sqlite3

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

def selectAllUserData():
    with app.app_context():
        cur = get_db().cursor()
        cur.execute("SELECT * FROM users")
        data = cur.fetchall()
        return data

def updatePercentage(percentage, id):
    with app.app_context():
        cur = get_db().cursor()
        cur.execute("UPDATE users SET percentage = ? WHERE ID = ?", (percentage, id))
        get_db().commit()
        cur.close()

## json

challengeFile = "challenge.json"
answerFile = "answer.json"

def challengeJson():
    with open(challengeFile, "r") as file:
        data = json.load(file)
        return data

def answerChallenge(userId, labId, status):

    new_entry = {
        "userId": userId,
        "labId": labId,
        "status": status
    }

    try:
        with open(answerFile, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(new_entry)

    with open(answerFile, "w") as file:
        json.dump(data, file, indent=4)

def lookupAnswerFile(userId):
    try:
        with open(answerFile, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    result = []
    for entry in data:
        if entry["userId"] == userId:
            result.append({
                "labId": entry["labId"],
                "status": entry["status"]
            })

    return result

def getChallenge():
    with open(challengeFile, "r") as file:
        data = json.load(file)
    return data
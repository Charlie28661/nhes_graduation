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
    
def selectAllUserId():
    with app.app_context():
        cur = get_db().cursor()
        cur.execute("SELECT ID FROM users")
        data = cur.fetchall()
        return data

def updatePercentage(percentage, id):
    with app.app_context():
        cur = get_db().cursor()
        cur.execute("UPDATE users SET percentage = ? WHERE ID = ?", (percentage, id))
        get_db().commit()
        cur.close()

def setPercentageZero():
    with app.app_context():
        cur = get_db().cursor()
        cur.execute("UPDATE users SET percentage = 0;")
        get_db().commit()
        cur.close()

## json

challengeFile = "challenge.json"
answerFile = "answer.json"
genFile = "gen_answer.json"

def challengeJson():
    with open(challengeFile, "r") as file:
        data = json.load(file)
        if data is None:
            pass
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
    except(FileNotFoundError, json.JSONDecodeError):
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

def addChallenge(labId, labName, labDescription, labScore, labActive):

    new_entry = {
        "labId": int(labId),
        "name": labName,
        "description": labDescription,
        "score": int(labScore),
        "active": labActive
    }

    try:
        with open(challengeFile, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(new_entry)

    with open(challengeFile, "w") as file:
        json.dump(data, file, indent=4)


def updateLab(labId, labName, labDescription, labScore, labActive):

    with open(challengeFile, "r") as file:
        data = json.load(file)

    for challenge in data:
        if int(labId) == int(challenge["labId"]):
            challenge["labId"] = int(labId)
            challenge["name"] = labName
            challenge["description"] = labDescription
            challenge["score"] = int(labScore)
            challenge["active"] = labActive
            break

    with open(challengeFile, 'w') as f:
        json.dump(data, f, indent=4)

def showAllChallenge():

    with open(challengeFile, "r") as file:
        data = json.load(file)

    for hideChallenge in data:
        hideChallenge["active"] = "Visible"

    with open(challengeFile, 'w') as f:
        json.dump(data, f, indent=4)

def hideAllChallenge():
    with open(challengeFile, "r") as file:
            data = json.load(file)

    for hideChallenge in data:
        hideChallenge["active"] = "Invisible"

    with open(challengeFile, 'w') as f:
        json.dump(data, f, indent=4)

def addAnsCode(labId, code, userName):

    new_entry = {
        "labId": int(labId),
        "code": code,
        "genBy": userName,
        "used": 0
    }

    try:
        with open(genFile, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(new_entry)

    with open(genFile, "w") as file:
        json.dump(data, file, indent=4)

def updateGenFile(labId, getAns, username):

    try:
        with open(genFile, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        status = 0
        return status

    updated = False
    for check in data:
        if int(labId) == int(check["labId"]) and str(getAns) == str(check["code"]) and check["used"] != 1:
            check["used"] = 1
            updated = True
            break

    if updated:
        with open(genFile, 'w') as f:
            json.dump(data, f, indent=4)
            answerChallenge(int(username), int(labId), "Completed")
        return True
    else:
        return False
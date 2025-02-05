import db
from flask import g
from flask import Flask
from flask import url_for
from flask import session
from flask import request
from flask import redirect
from flask import render_template


app = Flask(__name__)
app.secret_key = "NHES"

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

@app.route("/", methods = ["GET", "POST"])
@app.route("/login", methods = ["GET", "POST"])
def login():

    username = session.get("username")
    if "username" in session:
        return redirect(url_for("dashboard"))

    error = None
    if request.method == "POST":
        userId = request.values["userid"]
        password = request.values["password"]

        userData = db.selectUserDataById(userId)

        if userData is not None:
            if userId == userData[0] and password == userData[1]:
                session["username"] = userId

                return redirect(url_for("dashboard"))
            else:
                error = "請輸入正確帳號密碼"

    return render_template("login.html", **locals())

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/dashboard")
def dashboard():

    username = session.get("username")
    if "username" not in session:
        return redirect(url_for("login"))

    userData = db.selectUserDataById(username)
    userId = userData[0]
    userName = userData[2]
    userRole = userData[3]

    if userRole == "student":
        userRole = "學生"
    elif userRole == "teacher":
        userRole = "教師"

    allChallenge = db.challengeJson()
    checkAnswerStatus = db.lookupAnswerFile(int(userId))

    if allChallenge:
        maxChallenge = max(allChallenge, key=lambda x: x["labId"])["labId"]
        percentage = (len(checkAnswerStatus) / maxChallenge) * 100
        percentage = int(percentage)
        db.updatePercentage(percentage, userId)
    else:
        maxChallenge = None

    for challenge in allChallenge:
        challenge["completed"] = any(
            answerStatus["labId"] == challenge["labId"] and answerStatus["status"] == "Completed"
            for answerStatus in checkAnswerStatus
        )

    return render_template("dashboard.html", **locals())

@app.route("/admin", methods = ["GET", "POST"])
def admin():

    admin = session.get("admin")
    if "admin" in session:
        return redirect(url_for("adminPanel"))

    if request.method == "POST":
        adminId = request.values["adminId"]
        password = request.values["password"]

        userData = db.selectUserDataById(adminId)

        if userData is not None:
            if adminId == userData[0] and password == userData[1] and userData[3] == "admin":
                session["admin"] = adminId
                return redirect(url_for("adminPanel"))
            else:
                return render_template("admin.html")

    return render_template("admin.html")

@app.route("/adminPanel", methods = ["GET", "POST"])
def adminPanel():

    admin = session.get("admin")
    if "admin" not in session:
        return redirect(url_for("admin"))

    getAllUserData = db.selectAllUserData()
    allChallenge = db.challengeJson()
    if allChallenge:
        maxChallenge = max(allChallenge, key=lambda x: x["labId"])["labId"]
    else:
        maxChallenge = 0

    if request.method == "POST":
        labId = request.values["labId"]
        labName = request.values["name"]
        labDescription = request.values["description"]
        labScore = request.values["score"]
        labActive = request.values["active"]

        labId = int(labId)

        if len(labName) == 0:
            labName = str(allChallenge[labId-1]["name"])

        if len(labDescription) == 0:
            labDescription = str(allChallenge[labId-1]["description"])

        if labId > maxChallenge:
            db.addChallenge(labId, labName, labDescription, labScore, labActive)
            return redirect(url_for("adminPanel"))
        else:
            db.updateLab(labId, labName, labDescription, labScore, labActive)
            return redirect(url_for("adminPanel"))


    return render_template("adminPanel.html", **locals())

@app.route("/scoreboard")
def scoreboard():

    getAllUserData = db.selectAllUserData()

    return render_template("scoreboard.html", **locals())


@app.route("/setPercentageZero")
def setPercentageZero():

    admin = session.get("admin")
    if "admin" not in session:
        return redirect(url_for("admin"))

    db.setPercentageZero()
    return redirect(url_for("adminPanel"))

@app.route("/showAllChallenge")
def showAllChallenge():

    admin = session.get("admin")
    if "admin" not in session:
        return redirect(url_for("admin"))

    db.showAllChallenge()
    return redirect(url_for("adminPanel"))

@app.route("/hideAllChallenge")
def hideAllChallenge():

    admin = session.get("admin")
    if "admin" not in session:
        return redirect(url_for("admin"))

    db.hideAllChallenge()
    return redirect(url_for("adminPanel"))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5800, debug=True)
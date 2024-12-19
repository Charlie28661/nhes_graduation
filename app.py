import db
from flask import Flask
from flask import url_for
from flask import session
from flask import request
from flask import redirect
from flask import render_template

app = Flask(__name__)
app.secret_key = "NHES"

@app.route("/", methods = ["GET", "POST"])
@app.route("/login", methods = ["GET", "POST"])
def login():

    if request.method == "POST":
        userId = request.values["userid"]
        password = request.values["password"]
        session["username"] = userId
        return redirect(url_for("dashboard"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/dashboard")
def dashboard():

    username = session.get("username")
    if "username" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html", **locals())

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5800, debug=True)
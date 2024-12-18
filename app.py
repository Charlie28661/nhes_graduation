import db
import flask
from flask import render_template
app = flask.Flask(__name__)

@app.route("/")
def index():
    return render_template("login.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5500, debug=True)
from flask import render_template
from project import app

@app.route("/", methods = ["GET"])
def index():
    return render_template("index.html")
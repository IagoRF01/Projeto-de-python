from flask import render_template
from database import app

@app.route("/")
def home():
    return render_template("index.html")
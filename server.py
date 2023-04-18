"""Server for occasion reminders app."""

import requests
from flask import (Flask, render_template, request,flash,session,redirect)
from model import connect_to_db,db
import crud

app = Flask(__name__)

@app.route('/')
def homepage():
    """Landing page"""
    return render_template("homepage.html")

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", port = 5050, debug=True)
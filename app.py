from flask import Flask, request, url_for, session, redirect

app = Flask(__name__)

@app.route("/")
def test_statement():
    return "sup bitches"

@app.route("/yikes")
def new_statement():
    return "ohno"
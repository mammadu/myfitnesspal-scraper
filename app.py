from flask import Flask, request, url_for, session, redirect, render_template

app = Flask(__name__)

@app.route("/")
def index():
    oauth_address = url_for('oauth')
    return f"<a href={oauth_address}> oauth login</a>"

@app.route("/oauth")
def oauth():
    return "ohno"

@app.route("/success")
def suscess():
    return "Successful redirection!"

if __name__ == "__main__":
    app.run(ssl_context='adhoc') #doesn't seem to make the server run using https. Use "flask run --cert=adhoc" on the command line to enable https
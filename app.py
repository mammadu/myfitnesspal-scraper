from flask import Flask, request, url_for, session, redirect, render_template
import json

app = Flask(__name__)

@app.route("/")
def index():
    oauth_address = url_for('oauth')
    return f"<a href={oauth_address}> oauth login</a>"

@app.route("/oauth")
def oauth():
    with open('client_ID.json') as client_id:
        data = json.load(client_id)
    
    auth_uri = data["web"]["auth_uri"]
    client_id = data["web"]["client_id"]
    redirect_uris = data["web"]["redirect_uris"]
    #need to creadte redirect uri
    print(data["web"]["project_id"])
    return data

@app.route("/success")
def suscess():
    return "Successful redirection!"

if __name__ == "__main__":
    app.run(ssl_context='adhoc') #doesn't seem to make the server run using https. Use "flask run --cert=adhoc" on the command line to enable https
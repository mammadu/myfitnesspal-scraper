from flask import Flask, request, url_for, session, redirect, render_template
import json

app = Flask(__name__)

@app.route("/")
def index():
    oauth_address = url_for('oauth')
    return f"<a href={oauth_address}>login</a>"

@app.route("/oauth")
def oauth():
    with open('client_ID.json') as client_id:
        data = json.load(client_id)
    
    auth_uri = data["web"]["auth_uri"]
    client_id = data["web"]["client_id"]
    redirect_uris = data["web"]["redirect_uris"][0]
    total_auth_uri = auth_uri + "?" + "response_type=code" + "&" + f"client_id={client_id}" + "&" + f"redirect_uri={redirect_uris}" + "&" + "scope=https://www.googleapis.com/auth/fitness.nutrition.read" + "&" + "state=1234"

    # print(total_auth_uri)
    return f"<a href={total_auth_uri}/> oauth</a>"

@app.route("/success")
def success(): #need to determine how to use get code and exchange for access token
    return "Successful redirection!"

if __name__ == "__main__":
    app.run(ssl_context='adhoc') #doesn't seem to make the server run using https. Use "flask run --cert=adhoc" on the command line to enable https
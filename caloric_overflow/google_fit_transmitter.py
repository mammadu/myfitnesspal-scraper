# overall flow
# Create url for user authorization
# Create browser that goes to url
# user gives Authorization
# Start flask server located at redirect uri
# Browser sends authorization code to redirect uri
# Flask server gets authorization code at redirect uri
# Close flask server
# Send POST request with authorization code to get authorization token
# Use authorization token to write nutritional data to google fit


from flask import Flask, request, url_for, session, redirect, render_template
import json, requests, random, webbrowser, subprocess

# app = Flask(__name__)

# @app.route("/")
# def index():
#     oauth_address = url_for('oauth')
#     return f"<a href={oauth_address}>login</a>"



# @app.route("/oauth")
def create_oauth_url(filepath):
    with open(filepath) as client_id:
        data = json.load(client_id)

    auth_uri = data["web"]["auth_uri"]
    client_id = data["web"]["client_id"]
    redirect_uris = data["web"]["redirect_uris"][0]
    response_type = "code"
    randstate = str(random.randrange(1000))

    query_dict = {
        "response_type": response_type,
        "client_id": client_id,
        "redirect_uri": redirect_uris,
        "scope": "https://www.googleapis.com/auth/fitness.nutrition.read",
        "state": randstate
    }

    total_auth_uri = auth_uri + "?" + list(query_dict.items())[0][0] + "=" + list(query_dict.items())[0][1]
    for i in range (1, len(query_dict)):
        total_auth_uri = total_auth_uri + "&" + list(query_dict.items())[i][0] + "=" + list(query_dict.items())[i][1]
    return total_auth_uri

filepath = '../client_ID.json'
url = create_oauth_url(filepath)
server = subprocess.Popen(['/usr/bin/python3', './server_receiver.py'])
print(server.pid)
webbrowser.open_new(url)
print(server.poll())




# @app.route("/success")
# def success(): 
#     code = request.args.get('code')

#     with open('../client_ID.json') as client_id:
#         data = json.load(client_id)
#     token_uri = data["web"]["token_uri"]
#     client_id = data["web"]["client_id"]
#     redirect_uris = data["web"]["redirect_uris"][0]
#     client_secret = data["web"]["client_secret"]

#     query_dict = {
#         "code": code,
#         "redirect_uri": redirect_uris,
#         "client_id": client_id,
#         "client_secret": client_secret,
#         "grant_type": "authorization_code",
#     }
#     r = requests.post(token_uri, params = query_dict)
#     print(r.text)
#     access_token = r.json()['access_token']
    
#     request_uri = "https://www.googleapis.com/fitness/v1/users/me/dataSources"
#     headers = {
#         "Authorization": f"Bearer {access_token}"
#     }
#     p = requests.get(request_uri, headers = headers)
#     print(p.text)
#     return "Successful redirection!"

# #Need to determine how to get nutrional data


# if __name__ == "__main__":
#     app.run(ssl_context='adhoc') #doesn't seem to make the server run using https. Use "flask run --cert=adhoc" on the command line to enable https
#!/usr/bin/python3

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
from datetime import datetime
import json, requests, random, webbrowser, subprocess, os, time, string, hashlib, base64

def create_code_verifier(code_size):
    allowed_chars = string.ascii_letters + string.digits + '-._~'
    code_verifier = ''.join(random.choice(allowed_chars) for i in range(code_size))
    return code_verifier

def create_code_challenge(code_verifier):
    code_verifier_to_bytes = code_verifier.encode('utf-8') #convert code_verifier to bytes
    hashed_object = hashlib.sha256(code_verifier_to_bytes) #create hash object from code_verifier_byres
    digest_hashed_str = hashed_object.digest() #get hashed_object in bytes
    base64_hexdigest_hashed_str = base64.urlsafe_b64encode(digest_hashed_str) #convert byte object to base64 byte string
    code_challenge = str(base64_hexdigest_hashed_str, 'utf-8') #create utf-8 string from byte string
    code_challenge = code_challenge[:-1] #for some reason, an '=' is added to the end of the code string, this line removes it
    return code_challenge

def create_oauth_url(filepath):
    with open(filepath) as client_id:
        data = json.load(client_id)

    auth_uri = data["web"]["auth_uri"]
    client_id = data["web"]["client_id"]
    redirect_uris = data["web"]["redirect_uris"][0]
    response_type = "code"
    randstate = str(random.randrange(1000))
    code_verifier = create_code_verifier(100)
    code_challenge = create_code_challenge(code_verifier)

    query_dict = {
        "response_type": response_type,
        "client_id": client_id,
        "redirect_uri": redirect_uris,
        "scope": "https://www.googleapis.com/auth/fitness.nutrition.read",
        "state": randstate,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256"
    }

    total_auth_uri = auth_uri + "?" + list(query_dict.items())[0][0] + "=" + list(query_dict.items())[0][1]
    for i in range (1, len(query_dict)):
        total_auth_uri = total_auth_uri + "&" + list(query_dict.items())[i][0] + "=" + list(query_dict.items())[i][1]
    return total_auth_uri

def get_authorization_code():
    filepath = '../client_ID.json'
    url = create_oauth_url(filepath)
    current_time = time.time()
    server = subprocess.Popen(['/usr/bin/python3', './server_receiver.py'])
    webbrowser.open_new(url)

    while (current_time > os.path.getmtime("authorization_code.txt")):
        continue

    time.sleep(1)
    server.kill()

# def create_token_url(filepath):
#     with open(filepath) as client_id:
#         data = json.load(client_id)

#     token_uri = data["web"]["token_uri"]
#     client_id = data["web"]["client_id"]
#     code = ""
#     randstate = str(random.randrange(1000))
#     code_verifier = create_code_verifier(100)
#     print(f"code_verifier = {code_verifier}")

#     code_challenge = create_code_challenge(code_verifier)
#     print(f"code_challenge = {code_challenge}")

#     query_dict = {
#         "response_type": response_type,
#         "client_id": client_id,
#         "redirect_uri": redirect_uris,
#         "scope": "https://www.googleapis.com/auth/fitness.nutrition.read",
#         "state": randstate,
#         "code_challenge": code_challenge,
#         "code_challenge_method": "S256"
#     }

#     total_token_uri = token_uri + "?" + list(query_dict.items())[0][0] + "=" + list(query_dict.items())[0][1]
#     for i in range (1, len(query_dict)):
#         total_auth_uri = total_auth_uri + "&" + list(query_dict.items())[i][0] + "=" + list(query_dict.items())[i][1]
#     return total_auth_uri

get_authorization_code()

# print("hashed_code = ", hashed_code)



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


import json, requests, random, webbrowser, subprocess, os, time, string, hashlib, base64, pathlib, sys

path = pathlib.Path(__file__)

def create_code_verifier(code_size):
    allowed_chars = string.ascii_letters + string.digits + '-._~'
    code_verifier = ''.join(random.choice(allowed_chars) for i in range(code_size))
    return code_verifier

# def create_code_challenge(code_verifier):
#     code_verifier_to_bytes = code_verifier.encode('utf-8') #convert code_verifier to bytes
#     hashed_object = hashlib.sha256(code_verifier_to_bytes) #create hash object from code_verifier_byres
#     digest_hashed_str = hashed_object.digest() #get hashed_object in bytes
#     base64_hexdigest_hashed_str = base64.urlsafe_b64encode(digest_hashed_str) #convert byte object to base64 byte string
#     code_challenge = str(base64_hexdigest_hashed_str, 'utf-8') #create utf-8 string from byte string
#     code_challenge = code_challenge[:-1] #for some reason, an '=' is added to the end of the code string, this line removes it
#     return code_challenge

def create_oauth_url(filepath):
    with open(filepath) as client_id:
        data = json.load(client_id)

    auth_uri = data["web"]["auth_uri"]
    client_id = data["web"]["client_id"]
    redirect_uris = data["web"]["redirect_uris"][0]
    response_type = "code"
    scope_list = [
        "https://www.googleapis.com/auth/fitness.nutrition.read",
        "https://www.googleapis.com/auth/fitness.nutrition.write",
        "https://www.googleapis.com/auth/fitness.body.read"
        ]
    scope = ' '.join(scope_list)
    randstate = str(random.randrange(1000))
    
    #debug
    # code_verifier = create_code_verifier(100)
    # with open("code_verifier.txt", "w") as file:
    #     file.write(code_verifier)
    # code_challenge = create_code_challenge(code_verifier)

    query_dict = {
        "response_type": response_type,
        "client_id": client_id,
        "redirect_uri": redirect_uris,
        "scope": scope,
        "state": randstate,
        
        
        #debug
        # "code_challenge": code_challenge, 
        # "code_challenge_method": "S256"
    }

    total_auth_uri = auth_uri + "?" + list(query_dict.items())[0][0] + "=" + list(query_dict.items())[0][1]
    for i in range (1, len(query_dict)):
        total_auth_uri = total_auth_uri + "&" + list(query_dict.items())[i][0] + "=" + list(query_dict.items())[i][1]
    return total_auth_uri

def get_authorization_code():
    filepath = str(path.resolve().parent.parent.joinpath('client_ID.json'))
    url = create_oauth_url(filepath)
    # print(url) #debug
    current_time = time.time()
    server = subprocess.Popen([sys.executable, './server_receiver.py'])
    webbrowser.open_new(url)

    while (current_time > os.path.getmtime("authorization_code.txt")):
        continue

    time.sleep(1)
    server.kill()

def create_token_url(filepath):
    with open(filepath) as client_id:
        data = json.load(client_id)

    token_uri = data["web"]["token_uri"]
    return token_uri

def token_post_param(filepath): 
    with open(filepath) as client_id:
        data = json.load(client_id)

    grant_type = "authorization_code"
    with open("authorization_code.txt", "r") as file:
        code = file.read()
    redirect_uris = data["web"]["redirect_uris"][0]
    client_id = data["web"]["client_id"]
    client_secret = data["web"]["client_secret"] 
    #debug
    # with open("code_verifier.txt", "r") as file:
    #     code_verifier = file.read()

    query_dict = {
        "grant_type": grant_type,
        "code": code,
        "redirect_uri": redirect_uris,
        "client_id": client_id,
        "client_secret": client_secret
        # , "code_verifier": code_verifier #debug
    }

    return query_dict

def get_access_token(): #I will eventually have to make a remote server get the access token to keep the client_secret private
    filepath = '../client_ID.json'
    url = create_token_url(filepath)
    query_dict = token_post_param(filepath)
    response = requests.post(url, data = query_dict)
    token = response.json()['access_token']
    return token

def get_google_fit_data():
    get_authorization_code()
    access_token = get_access_token()
    headers = {
        "access_token": access_token
    }

    goole_fit_base = "https://www.googleapis.com/fitness/v1/users/me"
    data_type = "dataSources"
    # dataSourceID = "raw:com.google.weight:com.qingniu.arboleaf:weight"
    dataSourceID = "com.google.weight:com.qingniu.arboleaf"
    datasets = "datasets"
    minimumDate = "652222439"
    maximumDate = "1636923239"
    date_range = '-'.join([minimumDate, maximumDate])
    url_component_list = [
        goole_fit_base
        , data_type
        , dataSourceID
        , datasets
        , date_range
    ]

    total_url = '/'.join(url_component_list)

    response = requests.get(total_url, headers)
    print(response)
    print(response.text)
    return response.text

with open("google_fit_transmitter.json", "w") as file:
    file.write(get_google_fit_data())
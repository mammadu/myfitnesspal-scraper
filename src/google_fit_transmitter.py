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


import json, requests, random, webbrowser, subprocess, os, time, pathlib, sys

path = pathlib.Path(__file__)

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
        "https://www.googleapis.com/auth/fitness.body.read",
        "https://www.googleapis.com/auth/fitness.body.write"
        ]
    scope = ' '.join(scope_list)
    randstate = str(random.randrange(1000))

    query_dict = {
        "response_type": response_type,
        "client_id": client_id,
        "redirect_uri": redirect_uris,
        "scope": scope,
        "state": randstate,
    }

    total_auth_uri = auth_uri + "?" + list(query_dict.items())[0][0] + "=" + list(query_dict.items())[0][1]
    for i in range (1, len(query_dict)):
        total_auth_uri = total_auth_uri + "&" + list(query_dict.items())[i][0] + "=" + list(query_dict.items())[i][1]
    return total_auth_uri

def get_authorization_code():
    filepath = str(path.resolve().parent.parent.joinpath('client_ID.json'))
    url = create_oauth_url(filepath)
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

    query_dict = {
        "grant_type": grant_type,
        "code": code,
        "redirect_uri": redirect_uris,
        "client_id": client_id,
        "client_secret": client_secret
    }

    return query_dict

def get_access_token(): #I will eventually have to make a remote server get the access token to keep the client_secret private
    filepath = '../client_ID.json'
    url = create_token_url(filepath)
    query_dict = token_post_param(filepath)
    response = requests.post(url, data = query_dict)
    token = response.json()['access_token']
    return token

def create_access_token_header():
    get_authorization_code()
    access_token = get_access_token()
    headers = {
        "access_token": access_token
    }
    return headers

def compose_url(url_base, path_list):
    url_components = path_list.copy()
    url_components.insert(0,url_base)
    total_url = '/'.join(url_components)
    return total_url

#Functions to implement
def create_datasource(data):
    google_fit_base = "https://www.googleapis.com/fitness/v1/users/me"
    datasource = "dataSources"
    url_component_list = [datasource]
    total_url = compose_url(google_fit_base, url_component_list)
    print(f"total_url = {total_url}")

    headers = create_access_token_header()
    response = requests.post(total_url, json=data, params=headers)
    print(response) #debug
    return response.text

def delete_datasource(datasource_id):
    google_fit_base = "https://www.googleapis.com/fitness/v1/users/me"
    datasource = "dataSources"
    url_component_list = [datasource, datasource_id]
    total_url = compose_url(google_fit_base, url_component_list)
    print(f"total_url = {total_url}")

    headers = create_access_token_header()
    response = requests.delete(total_url, params=headers)
    print(response) #debug
    return response.text

def get_list_of_datasources():
    google_fit_base = "https://www.googleapis.com/fitness/v1/users/me"
    datasource = "dataSources"
    url_component_list = [datasource]
    total_url = compose_url(google_fit_base, url_component_list)
    print(f"total_url = {total_url}")

    headers = create_access_token_header()
    response = requests.get(total_url, headers)
    print(response) #debug
    return response.text

def get_dataset(datasource_id, dataset_id):
    headers = create_access_token_header()

    google_fit_base = "https://www.googleapis.com/fitness/v1/users/me"
    datasource = "dataSources"
    datasets = "datasets"
    url_component_list = [
        datasource
        , datasource_id
        , datasets
        , dataset_id
    ]
    total_url = compose_url(google_fit_base, url_component_list)
    print(f"total_url = {total_url}")

    response = requests.get(total_url, params=headers)
    print(response) #debug
    return response.text

# def patch_dataset():


# def aggregate():

# debug. Currently testing get_dataset function
if __name__ == "__main__":
    data = {
        "application": {
            "name": "test"
        },
        "dataType": {
            "field": [
            {
                "name": "nutrients",
                "format": "map"
            },
            {
                "name": "meal_type",
                "format": "integer",
                "optional": True
            },
            {
                "name": "food_item",
                "format": "string",
                "optional": True
            }
            ],
            "name": "com.google.nutrition"
        },
        # "device": {
        #     # "manufacturer": "n/a",
        #     # "model": "n/a",
        #     # "type": "unknown",
        #     # "uid": "",
        #     # "version": ""
        # },
        "type": "derived"
    }
    with open("google_fit_transmitter.json", "w") as file:
        # file.write(create_datasource(data))
        # file.write(get_list_of_datasources())
        # file.write(get_dataset("derived:com.google.nutrition:3d54f750:n/a:n/a:18a3e27c", "*"))
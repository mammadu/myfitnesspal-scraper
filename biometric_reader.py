import requests

client_id = '420385216741-1qc1r02ff6jluk28q00mmlu4vs21mbig.apps.googleusercontent.com'

url = f'https://www.googleapis.com/fitness/v1/users/me/dataSources/'

resp = requests.get(url, auth=(client_id))
if resp.status_code != 200:
    print("there was an error")
    print("response status code =")
    print(resp.status_code)
else:
    print('success')
    print('resp.status_code =', resp.status_code)
    print(resp.headers)
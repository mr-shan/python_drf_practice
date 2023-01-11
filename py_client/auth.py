import requests

from getpass import getpass

auth_endpoint = "http://127.0.0.1:8000/api/auth/"

def get_auth_token():
    username = input("Please enter your username: ")
    password = getpass("Please enter your password: ")

    auth_data = {
        'username': username,
        'password': password
    }

    auth_response = requests.post(auth_endpoint, data=auth_data)

    if auth_response.status_code == 200:
        return auth_response.json()['token']
    else:
        return None
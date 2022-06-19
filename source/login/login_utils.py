import requests, base64, pickle
from typing import List

def get_login_details(data: str) -> str:
    """Return username and decoded password from binary file"""
    username = data[0]
    password = data[1]
    decoded_password = bytes(base64.b64decode(password.decode('utf-8'))).decode("utf8")
    return username, decoded_password

def login(username: str, password: str) -> bool:
    """Return request status for login"""
    response = requests.post('https://cbauth.herokuapp.com/', data={'discord':'{}'.format(username), 'password':'{}'.format(password)})
    if response.text == 'passed':
        return True
    else:
        return False

def writebinary(file: str, details: List) -> None:
    """Writes a binary file to a given location with the given details"""
    with open(file, 'wb') as f:
        pickle.dump(details, f)
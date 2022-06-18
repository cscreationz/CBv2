import requests
import base64

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
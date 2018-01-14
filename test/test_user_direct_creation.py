import time
import auth
import requests
import c
import com

headers = {}


def setup_module(module):
    global headers
    headers = {"Api-key": auth.auth()}


def get_files():
    front = open('/tmp/a.png')
    back = open('/tmp/a.png')
    files = {
        'front': front, 'back': back
    }
    return files


def test_user_create_direct():
    name = 'test_e' + str(int(round(time.time() * 1000))) + "@maxmoney.com"
    url = "/users/create-user"
    data = {'idNo': 321234561112, 'username': name, 'name': "Test User",
            'password': 'junk', 'mobile': '+919845104104',
            'role': 'maxCddOfficer', 'email': name
            }
    files = get_files()
    response = requests.post(c.site + url, verify=False, headers=headers, data=data, files=files)
    assert response.status_code == 200
    files = get_files()
    response = requests.post(c.site + url, verify=False, headers=headers, data=data, files=files)
    assert response.status_code == 409


test_user_create_direct()

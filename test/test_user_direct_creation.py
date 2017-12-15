
import time
import auth
import requests
import c

headers = {}


def setup_module(module):
    global headers
    headers = {"Api-key":auth.auth()}


def test_user_create_direct():
    front = open('/tmp/a.png')
    back = open('/tmp/a.png')
    print front
    name = 'teste' + str(int(round(time.time() * 1000))) + "@maxmoney.com"
    url = "/users/create-user"
    data = {'idNo': 321234561112,'username': name,'name': name,
                             'password': 'junk','mobile': '+919845104104',
                             'role': 'maxCddOfficer','email' : name
                             }
    files = {
        'front' : front,'back' : back
    }
    response = requests.post(c.site + url, verify=False, headers=headers, data=data,files= files)
    print response

#setup_module(None)
test_user_create_direct()
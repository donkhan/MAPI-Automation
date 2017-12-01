import requests
import warnings
import time
import c
import auth

headers = {}

def setup_module(module):
    global headers
    headers = {"Api-key":auth.auth()}


def test_list_accounts():
    response = requests.get(c.site + "/topup/accounts", verify=False,headers = headers)
    assert response.status_code == 200


def test_update_account():
    response = requests.put(c.site + "/topup/accounts/account/sa@maxmoney.com", verify=False, headers=headers, data={'creditLimit':1000})
    assert response.status_code == 200
    assert response.json()['creditLimit'] == 1000


def test_create_account():
    name = 'test' + str(int(round(time.time() * 1000))) + "@maxmoney.com"
    response = requests.post(c.site + "/topup/accounts/account", verify=False, headers=headers,
                            data={'creditLimit': 1000,'creditAllowed' : 'true','accountName': name,
                                  'amount':1000,'status' : 'Active'})
    assert response.status_code == 200
    assert response.json()['creditLimit'] == 1000
    response = requests.post(c.site + "/topup/accounts/account", verify=False, headers=headers,
                  data={'creditLimit': 1000, 'creditAllowed': 'true', 'accountName': name,
                        'amount': 1000, 'status': 'Active'})
    assert response.status_code == 400


def main():
    global headers
    try:
        headers = {"Api-Key":auth.auth()}
        test_list_accounts()
        test_update_account()
    except:
        print 'Sorry Unable to execute test cases'


if __name__ == "__main__":
    main()
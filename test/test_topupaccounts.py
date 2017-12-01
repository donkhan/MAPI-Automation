import requests
import warnings
import time
import c
import auth
import com

headers = {}

def setup_module(module):
    global headers
    headers = {"Api-key":auth.auth()}


def test_list_accounts():
    response = com.get("/topup/accounts", headers)
    assert response.status_code == 200


def test_update_account():
    response = com.put("/topup/accounts/account/sa@maxmoney.com",headers,{'creditLimit':1000})
    assert response.status_code == 200
    assert response.json()['creditLimit'] == 1000


def test_create_account():
    name = 'test' + str(int(round(time.time() * 1000))) + "@maxmoney.com"
    response = com.post( "/topup/accounts/account",headers,
                            {'creditLimit': 1000,'creditAllowed' : 'true','accountName': name,
                                  'amount':1000,'status' : 'Active'})
    assert response.status_code == 200
    assert response.json()['creditLimit'] == 1000
    response = com.post("/topup/accounts/account",headers,
                  {'creditLimit': 1000, 'creditAllowed': 'true', 'accountName': name,
                        'amount': 1000, 'status': 'Active'})
    assert response.status_code == 400


def main():
    global headers
    headers = {"Api-Key":auth.auth()}
    test_list_accounts()
    test_update_account()
    

if __name__ == "__main__":
    main()
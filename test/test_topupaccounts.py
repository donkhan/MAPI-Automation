import requests
import warnings

warnings.filterwarnings("ignore")

site = "https://api-staging.maxmoney.com/v1"
(u,p) = ("maxmoney","maxmoney@@1")

headers = {}


def auth():
    payload = { 'username' : 'sa@maxmoney.com', 'password' : 'MaxMoney@2016'}
    r = requests.post(site + "/sessions/current",data=payload,verify=False,auth=(u,p))
    if r.status_code == 200:
        return r.json().get('session')
    if r.status_code == 201:
        return auth()
    print r.status_code
    print r.content
    raise 'Auth Failure'


def setup_module(module):
    global headers
    headers = {"Api-key":auth()}


def test_list_accounts():
    response = requests.get(site + "/topup/accounts", verify=False,headers = headers)
    assert response.status_code == 200


def test_update_account():
    response = requests.put(site + "/topup/accounts/account/sa@maxmoney.com", verify=False, headers=headers, data={'creditLimit':1000})
    assert response.status_code == 200
    assert response.json()['creditLimit'] == 1000

def main():
    global headers
    try:
        headers = {"Api-Key":auth()}
        #test_list_accounts()
        test_update_account()
    except:
        print 'Sorry Unable to execute test cases'


if __name__ == "__main__":
    main()
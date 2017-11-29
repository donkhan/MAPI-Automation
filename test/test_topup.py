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


def test_indian_mobile():
    response = requests.get(site + "/topup/+919845104104/product", verify=False,headers = headers)
    assert response.status_code == 200


def test_non_exist_indian_mobile():
    response = requests.get(site + "/topup/+919845104104104/product", verify=False,headers = headers)
    assert response.status_code == 200
    assert response.json()['errorCode'] != 0


def test_operators_of_india():
    assert requests.get(site + "/topup/766/operators", verify=False, headers=headers).status_code == 200


def test_operators_of_non_existent_country():
    response = requests.get(site + "/topup/76600/operators", verify=False, headers=headers)
    print response.status_code
    assert response.status_code == 200
    assert response.json()['errorCode'] != 0


def test_products_of_operator():
    assert requests.get(site + "/topup/operator/1437/product", verify=False, headers=headers).status_code == 200


def test_products_of_nonexistent_operator():
    assert requests.get(site + "/topup/operator/1437000/product", verify=False, headers=headers).status_code == 200


def test_ping():
    assert requests.get(site + "/topup/ping", verify=False, headers=headers).status_code == 200


def main():
    global headers
    try:
        headers = {"Api-Key":auth()}
        test_ping()
        test_indian_mobile()
        test_non_exist_indian_mobile()
        test_operators_of_non_existent_country()
        test_products_of_operator()
        test_products_of_nonexistent_operator()

    except:
        print 'Sorry Unable to execute test cases'


if __name__ == "__main__":
    main()
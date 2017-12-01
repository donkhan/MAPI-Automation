import requests
import warnings
import auth
import c
warnings.filterwarnings("ignore")
headers = {}




def setup_module(module):
    global headers
    headers = {"Api-key":auth.auth()}


def test_indian_mobile():
    response = requests.get(c.site + "/topup/+919845104104/product", verify=False,headers = headers)
    assert response.status_code == 200


def test_malaysian_mobile():
    response = requests.get(c.site + "/topup/+60107860848/product", verify=False,headers = headers)
    assert response.status_code == 200


def test_non_exist_indian_mobile():
    response = requests.get(c.site + "/topup/+919845104104104/product", verify=False,headers = headers)
    assert response.status_code == 200
    assert response.json()['errorCode'] != 0


def test_operators_of_india():
    assert requests.get(c.site + "/topup/766/operators", verify=False, headers=headers).status_code == 200


def test_operators_of_non_existent_country():
    response = requests.get(c.site + "/topup/76600/operators", verify=False, headers=headers)
    print response.status_code
    assert response.status_code == 200
    assert response.json()['errorCode'] != 0


def test_products_of_operator():
    assert requests.get(c.site + "/topup/operator/1437/product", verify=False, headers=headers).status_code == 200


def test_products_of_nonexistent_operator():
    assert requests.get(c.site + "/topup/operator/1437000/product", verify=False, headers=headers).status_code == 200


def test_ping():
    assert requests.get(c.site + "/topup/ping", verify=False, headers=headers).status_code == 200


def main():
    global headers
    try:
        headers = {"Api-Key":auth.auth()}
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
import requests
import warnings

warnings.filterwarnings("ignore")

site = "https://api-staging.maxmoney.com/v1"
(u,p) = ("maxmoney","maxmoney@@1")


def print_response(text,response):
    print text
    print response.status_code
    print response.content


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
    raise('Auth Fails')


def setup_module(module):
    global headers
    headers = {"Api-key":auth()}


def test_indian_mobile():
    mobile_no = "+919845104104"
    response = requests.get(site + "/topup/"+mobile_no+"/product", verify=False,headers = headers)
    assert response.status_code == 200

def test_non_exist_indian_mobile():
    mobile_no = "+919845104104104"
    response = requests.get(site + "/topup/"+mobile_no+"/product", verify=False,headers = headers)
    assert response.status_code == 200

def get_operators_of_country(headers):
    print_response("Operators of India",requests.get(site + "/topup/766/operators", verify=False, headers=headers))


def get_products_of_operator(headers):
    print_response("Products of Operator with ID 1437",requests.get(site + "/topup/operator/1437/product", verify=False, headers=headers))



def ping(headers):
    print_response("Ping",requests.get(site + "/topup/ping", verify=False, headers=headers,
                     auth=('maxmoney', 'maxmoney@@1')))

def main():
    global headers
    try:
        headers = {"Api-Key":auth()}
        print headers
        #ping({'Api-Key': sessionid})
        test_indian_mobile()
        test_non_exist_indian_mobile()
        #get_operators_of_country({'Api-Key': sessionid})
        #get_products_of_operator({'Api-Key': sessionid})
    except:
        print 'Sorry Unable to execute test cases'

if __name__ == "__main__":
    main()
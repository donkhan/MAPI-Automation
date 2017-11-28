import requests
import warnings
warnings.filterwarnings("ignore")

site = "https://api-staging.maxmoney.com/v1"


def print_response(text,response):
    print text
    print response.status_code
    print response.content

def auth():
    payload = { 'username' : 'sa@maxmoney.com', 'password' : 'MaxMoney@2016'}
    r = requests.post(site + "/sessions/current",data=payload,verify=False,auth=('maxmoney','maxmoney@@1'))
    if r.status_code == 200:
        return r.json().get('session')
    if r.status_code == 201:
        return auth()
    print r.status_code
    print r.content
    raise('Auth Fails')


def get_product(headers):
    print_response("Products of +919845104104",requests.get(site + "/topup/+919845104104/product", verify=False,headers = headers,
                      auth=('maxmoney', 'maxmoney@@1')))


def get_operators_of_country(headers):
    print_response("Operators of India",requests.get(site + "/topup/766/operators", verify=False, headers=headers,
                     auth=('maxmoney', 'maxmoney@@1')))


def get_products_of_operator(headers):
    print_response("Products of Operator with ID 1437",requests.get(site + "/topup/operator/1437/product", verify=False, headers=headers,
                     auth=('maxmoney', 'maxmoney@@1')))


def ping(headers):
    print_response("Ping",requests.get(site + "/topup/ping", verify=False, headers=headers,
                     auth=('maxmoney', 'maxmoney@@1')))

def main():
    try:
        sessionid = auth()
        ping({'Api-Key': sessionid})
        get_product({'Api-Key': sessionid})
        get_operators_of_country({'Api-Key': sessionid})
        get_products_of_operator({'Api-Key': sessionid})
    except:
        print 'Sorry Unable to execute test cases'

if __name__ == "__main__":
    main()
import requests
import warnings
import time

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


def test_user_report_with_out_role():
    response = requests.post(site + "/reports/user", verify=False, headers=headers,
                            data={'from': "2017-1-1",'to':'2018-1-1','type':'csv'})
    print response.content
    assert response.status_code == 200


def test_user_report_with_role():
    response = requests.post(site + "/reports/user", verify=False, headers=headers,
                            data={'from': "2017-1-1",'to':'2018-1-1','type':'csv','role':'financeManager'})
    assert response.status_code == 200
    assert_role(response.content, "financeManager")


def test_user_report_with_customer():
    response = requests.post(site + "/reports/user", verify=False, headers=headers,
                            data={'from': "2017-1-1",'to':'2018-1-1','type':'csv','role':'customer'})
    assert response.status_code == 200
    assert_role(response.content,"customer")


def assert_role(content,role):
    lines = content.split("\n")
    for line in lines[1:len(lines)-1]:
        tokens = line.split(",")
        print tokens[0] + " -> " + tokens[2]
        assert tokens[2] == role


def main():
    global headers
    try:
        headers = {"Api-Key":auth()}
        test_user_report_with_out_role()
        test_user_report_with_role()
        test_user_report_with_customer()
    except:
        print 'Sorry Unable to execute test cases'


if __name__ == "__main__":
    main()
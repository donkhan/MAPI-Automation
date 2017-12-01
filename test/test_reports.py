import requests
import warnings
import datetime
import auth
import c

warnings.filterwarnings("ignore")
headers = {}


def setup_module(module):
    global headers
    headers = {"Api-key":auth.auth()}


def test_user_report_with_out_role():
    response = requests.post(c.site + "/reports/user", verify=False, headers=headers,
                            data={'from': "2017-1-1",'to':'2018-1-1','type':'csv'})

    assert response.status_code == 200
    lines = response.content.split("\n")
    for line in lines[1:len(lines) - 1]:
        tokens = line.split(",")
        print tokens[0] + " -> " + tokens[len(tokens)-1]


def test_user_report_with_role():
    response = requests.post(c.site + "/reports/user", verify=False, headers=headers,
                            data={'from': "2017-1-1",'to':'2018-1-1','type':'csv','role':'financeManager'})
    assert response.status_code == 200
    assert_role(response.content, "financeManager")


def test_user_report_with_customer():
    response = requests.post(c.site + "/reports/user", verify=False, headers=headers,
                            data={'from': "2017-1-1",'to':'2018-1-1','type':'csv','role':'customer'})
    assert response.status_code == 200
    assert_role(response.content,"customer")


def test_user_report_with_junk_to():
    response = requests.post(c.site + "/reports/user", verify=False, headers=headers,
                            data={'from': "2017-1-1",'to':'abcd','type':'csv','role':'customer'})
    print response.content
    assert response.status_code == 400


def assert_role(content,role):
    lines = content.split("\n")
    for line in lines[1:len(lines)-1]:
        tokens = line.split(",")
        print tokens[0] + " -> " + tokens[2]
        assert tokens[2] == role


def main():
    global headers
    headers = {"Api-Key":auth.auth()}
    print headers
    test_user_report_with_out_role()
    test_user_report_with_role()
    test_user_report_with_customer()
    test_user_report_with_junk_to()

if __name__ == "__main__":
    main()
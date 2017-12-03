import requests
import warnings
import datetime
import auth
import com
import pytest

warnings.filterwarnings("ignore")
headers = {}


def setup_module(module):
    global headers
    headers = {"Api-key":auth.auth()}


def test_user_report_with_out_role():
    response = com.post("/reports/user",headers,
                            {'from': "2017-1-1",'to':'2018-1-1','type':'csv'})
    print response.headers
    assert response.status_code == 200
    lines = response.content.split("\n")
    for line in lines[1:len(lines) - 1]:
        tokens = line.split(",")
        print tokens[0] + " -> " + tokens[len(tokens)-1]


def test_content_type():
    response = com.post("/reports/user", headers,
                        data={'from': "2017-1-1", 'to': '2018-1-1', 'type': 'csv', 'role': 'financeManager'})
    #assert response.headers['Content-Type'] == 'text'

@pytest.mark.parametrize("role", [
    "customer",
    "financeManager"
])
def test_role(role):
    response = com.post("/reports/user", headers,
                        data={'from': "2017-1-1", 'to': '2018-1-1', 'type': 'csv', 'role': role})
    assert response.status_code == 200


def test_user_report_with_junk_to():
    response = com.post("/reports/user",headers,
                            {'from': "2017-1-1",'to':'abcd','type':'csv','role':'customer'})
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
    test_content_type()
    test_user_report_with_out_role()
    test_role("customer")
    test_role("financeManager")
    test_user_report_with_junk_to()

if __name__ == "__main__":
    main()
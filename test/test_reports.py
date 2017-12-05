import requests
import warnings
import datetime
import auth
import com

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
    assert response.headers['Content-Type'] == 'text'


def test_user_report_with_role(role):
    response = com.post("/reports/user",headers,
                            data={'from': "2017-1-1",'to':'2018-1-1','type':'csv','role':role})
    assert response.status_code == 200
    assert_role(response.content, role)

def test_user_report_with_junk_to():
    response = com.post("/reports/user",headers,
                            {'from': "2017-1-1",'to':'abcd','type':'csv','role':'customer'})
    print response.content
    assert response.status_code == 400

def test_user_report_with_junk_from():
    response = com.post("/reports/user",headers,
                            {'from': "abcd",'to':'2018-1-1','type':'csv','role':'customer'})
    print response.content
    assert response.status_code == 400

def test_user_report_with_invalid_dates():
    response = com.post("/reports/user",headers,
                        {'from': '2018-1-1','to': '2017-1-1','type':'csv','role':'customer'})
    print response.content
    assert response.status_code == 400


def test_user_report_with_out_date():
    response = com.post("/reports/user", headers,
                        {'from': '', 'to': '', 'type': 'csv', 'role': 'customer'})
    print response.content
    assert response.status_code == 400


def test_user_report_with_out_from_date():
    response = com.post("/reports/user", headers,
                        {'from': '', 'to': '2018-1-1', 'type': 'csv', 'role': 'customer'})
    print response.content
    assert response.status_code == 400


def test_user_report_with_out_to_date():
    response = com.post("/reports/user", headers,
                        {'from': '2017-1-1', 'to': '', 'type': 'csv', 'role': 'customer'})
    print response.content
    assert response.status_code == 400

def test_user_report_with_invalid_from_date():
    response = com.post("/reports/user", headers,
                        {'from': '1000-1-1', 'to': '2018-1-1', 'type': 'csv', 'role': 'customer'})
    print response.content
    assert response.status_code == 400

def test_user_report_with_invalid_to_date():
    response = com.post("/reports/user", headers,
                        {'from': '2017-1-1', 'to': '3000-1-1', 'type': 'csv', 'role': 'customer'})
    print response.content
    assert response.status_code == 400

def test_user_report_with_invalid_dateFormat():
    response = com.post("/reports/user", headers,
                        {'from': '1-1-2017', 'to': '30-1-2018', 'type': 'csv', 'role': 'customer'})
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
    # test_content_type()
    # test_user_report_with_out_role()
    # test_user_report_with_role('financeManager')
    # test_user_report_with_role('customer')
    # test_user_report_with_junk_to()
    # test_user_report_with_junk_from()
    # test_user_report_with_invalid_dates()
    # test_user_report_with_out_date()
    # test_user_report_with_out_from_date()
    # test_user_report_with_out_to_date()
    # test_user_report_with_invalid_from_date()
    # test_user_report_with_invalid_to_date()
    # test_user_report_with_invalid_dateFormat()


if __name__ == "__main__":
    main()
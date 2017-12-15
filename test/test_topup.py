
import warnings
import auth
import com
warnings.filterwarnings("ignore")
headers = {}


def setup_module(module):
    global headers
    headers = {"Api-key":auth.auth()}


def test_indian_mobile():
    response = com.get("/topup/+919845104104/product",headers)
    assert response.status_code == 200


def test_junk_mobile():
    response = com.get("/topup/abcd/product",headers)
    assert response.status_code == 400


def test_malaysian_mobile():
    response = com.get("/topup/+60107860848/product",headers = headers)
    assert response.status_code == 200


def test_non_exist_indian_mobile():
    response = com.get("/topup/+919845104104104/product", headers)
    assert response.status_code == 200
    assert response.json()['errorCode'] != 0


def test_operators_of_india():
    assert com.get("/topup/766/operators", headers).status_code == 200


def test_operators_of_non_existent_country():
    response = com.get("/topup/76600/operators",headers)
    assert response.status_code == 200
    assert response.json()['errorCode'] != 0


def test_products_of_operator():
    assert com.get("/topup/operator/1437/product", headers).status_code == 200


def test_products_of_nonexistent_operator():
    assert com.get("/topup/operator/1437000/product", headers=headers).status_code == 200


def test_ping():
    assert com.get("/topup/ping",headers).status_code == 200


def test_topup_process():
    com.post("/topup",headers,{'mobileNo': "+919845104104",'senderMobileNo': '+919845104105','product': 100,
                               'retailPrice': 8.9,'serviceFee': '1'}).status_code == 200


def main():
    global headers
    headers = {"Api-Key":auth.auth()}
    test_topup_process()
    test_ping()
    test_indian_mobile()
    test_non_exist_indian_mobile()
    test_operators_of_non_existent_country()
    test_products_of_operator()
    test_products_of_nonexistent_operator()


if __name__ == "__main__":
    main()
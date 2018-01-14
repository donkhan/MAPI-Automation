import time
import auth
import com

headers = {}


def setup_module(module):
    global headers
    headers = {"Api-key":auth.auth()}


def test_finance_management():
    response = com.get("/topup/financial-position", headers)
    assert response.status_code == 200


import warnings
import auth
import com
warnings.filterwarnings("ignore")
headers = {}


def setup_module(module):
    global headers
    headers = {"Api-key":auth.auth()}


def test_rate_set():
    com.put("/boards/moos/rates/npr",headers,{'buy':'25','sell':'26','tt':'30','unit':1}).status_code == 200

def main():
    global headers
    headers = {"Api-Key":auth.auth()}
    test_rate_set()


if __name__ == "__main__":
    main()
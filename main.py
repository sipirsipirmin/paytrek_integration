import requests
from flask import Flask
from settings import SAMPLE_DATA, HEADERS, APIKEY_AND_SECRETKEY
from settings import SALE_CREATION_URL, CHARGE_URL, SALE_DETAILS_URL

app = Flask(__name__)


def create_sale():
    response = requests.post(
        SALE_CREATION_URL,
        data=SAMPLE_DATA,
        headers=HEADERS,
        auth=APIKEY_AND_SECRETKEY,
    )
    if response.status_code != 200:
        return False, response

    return True, response.json()


def make_payment(sale_token):
    payment_info = ''' {
        "number": "4508034508034509",
        "expiration": "12/2020",
        "cvc":"000",
        "card_holder_name":"John Doe",
        "sale_token":"%s"
    } ''' %(sale_token,)
    requests.post(
        CHARGE_URL,
        headers=HEADERS,
        data=payment_info,
        auth=APIKEY_AND_SECRETKEY,
    )
    return True


@app.route('/api/sale/<int:sale_id>/', methods=['GET'])
def get_sale(sale_id):
    '''
        This function returns sale_id' s detail in json format.
        if there is no sale_id lists all sale_id' s.
    '''
    response = requests.post(
        SALE_DETAILS_URL,
        data=SAMPLE_DATA,
        headers=HEADERS,
        auth=APIKEY_AND_SECRETKEY
    )

    return response.json()


@app.route('/api/make_sale/', methods=['POST'])
def make_sale():
    '''
        This function makes sale. Comminications paytrek sandbox.
        Creates sale object and makes payment.
    '''
    is_ok, dict_of_content = create_sale()
    if is_ok:
        make_payment(dict_of_content['sale_token'])

    return "200"


@app.route('/api/sales/', methods=['GET'])
def list_sales():
    response = requests.get(
        SALE_DETAILS_URL,
        headers=HEADERS,
        auth=APIKEY_AND_SECRETKEY
    )
    results = response.json()['results']
    temp = []
    for result in results:
        temp.append((
            result.get('created_at', 'Not Find'),
            result.get('sale_token', 'Not Find'),
            result.get('status', 'Not Find'),
        ))
        
    return str(temp)


if __name__ == '__main__':
    app.run()

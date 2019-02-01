import requests
from flask import Flask
from settings import  SAMPLE_DATA, HEADERS, APIKEY_AND_SECRETKEY

app = Flask(__name__)


def create_sale():
    sale_creation_url = 'https://sandbox.paytrek.com/api/v2/sale/'
    response = requests.post(
        sale_creation_url,
        data=SAMPLE_DATA,
        headers=HEADERS,
        auth=APIKEY_AND_SECRETKEY,
    )
    if response.status_code != 200:
        return False, response

    return True, response.json()


def make_payment(sale_token):
    payment_url = 'https://sandbox.paytrek.com/api/v2/charge/'
    payment_info = ''' {
        "number": "4508034508034509",
        "expiration": "12/2020",
        "cvc":"000",
        "card_holder_name":"John Doe",
        "sale_token":"%s"
    } ''' %(sale_token,)
    requests.post(
        payment_url,
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
    sale_details = 'https://sandbox.paytrek.com/api/v2/sale/'

    response = requests.post(
        sale_details,
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
    sale_details = 'https://sandbox.paytrek.com/api/v2/sale/'

    response = requests.get(
        sale_details,
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

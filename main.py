import requests
from flask import Flask
from flask import request
from requests.auth import HTTPBasicAuth


app = Flask(__name__)
SAMPLE_DATA = '''
{
  "amount": 24,
  "order_id": "1467034250",
  "secure_option": false,
  "pre_auth": false,
  "billing_address": "123 Market St. San Francisco",
  "billing_city": "San Francisco",
  "billing_country": "US",
  "billing_state": "CA",
  "currency": "TRY",
  "customer_email": "johndoe@gmail.com",
  "customer_first_name": "John",
  "customer_ip_address": "212.57.9.204",
  "customer_last_name": "Doe",
  "installment": 1,
  "items": [
    {
      "unit_price": 12,
      "quantity": 2,
      "name": "product_name",
      "photo": "https://sandbox.paytrek.com/statics/images/testing.jpg"
    }
  ],
  "sale_data": {
    "merchant_name": "Ted"
  }
}
'''
HEADERS = {
    'Content-Type': 'application/json',
}
APIKEY_AND_SECRETKEY = ('JwTKRgk+b2kdZjxrRO5VttbNVj/7dbfsLibdHFNWhJA=',
                                '67960ca449454654a78802362afc2559')


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
    response = requests.post(
        payment_url,
        headers=HEADERS,
        data=payment_info,
        auth=APIKEY_AND_SECRETKEY,
    )
    import ipdb; ipdb.set_trace()


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

    return str(response)


@app.route('/api/make_sale/', methods=['POST'])
def make_sale():
    '''
        This function makes sale. Comminications paytrek sandbox.
    '''
    is_ok, dict_of_content = create_sale()
    if is_ok:
        make_payment(dict_of_content['sale_token'])

    return "200"


if __name__ == '__main__':
    app.run()

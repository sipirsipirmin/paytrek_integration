import logging
import requests
from flask import Flask
from flask import request, jsonify
from settings import SAMPLE_DATA, HEADERS, APIKEY_AND_SECRETKEY
from settings import SALE_CREATION_URL, CHARGE_URL, SALE_DETAILS_URL

app = Flask(__name__)
logging.basicConfig(filename='main.log',level=logging.DEBUG)


def create_sale():
    '''
    Creates sale object in Paytrek server and gets this objects information.
    '''
    response = requests.post(
        SALE_CREATION_URL,
        data=SAMPLE_DATA,
        headers=HEADERS,
        auth=APIKEY_AND_SECRETKEY,
    )
    if response.status_code != 200:
        return False, response

    return True, response.json()


def make_payment(card_info):
    '''
    This function makes payment for created sale object.
    Params:
        card_info: which includes credit/debit card information and
            sale token(from sale object)
    '''
    response = requests.post(
        CHARGE_URL,
        headers=HEADERS,
        data=card_info,
        auth=APIKEY_AND_SECRETKEY,
    )
    return response


@app.route('/api/sale/<sale_token>/', methods=['GET'])
def get_sale(sale_token):
    '''
        This function returns sale object detail in json format which has
        given sale_token.
    '''
    try:
        response = requests.get(
            SALE_DETAILS_URL + sale_token,
            headers=HEADERS,
            auth=APIKEY_AND_SECRETKEY
        )
    except Exception as e:
        logging.error(e)
        return "Something went wrong. Please contact your business partner"

    return jsonify(response.json())


@app.route('/api/make_sale/', methods=['POST'])
def make_sale():
    '''
        This function makes sale. Comminicates paytrek sandbox.
        Creates sale object and makes payment.
    '''
    purchased_product_list = [i for i in request.values \
                                                if i.startswith('product')]
    is_ok, dict_of_content = create_sale()
    try:
        card_info = ''' {
            "number": "%s",
            "expiration": "%s/%s",
            "cvc":"%s",
            "card_holder_name":"%s",
            "sale_token":"%s"
        } ''' %(request.values['card_number'],
                request.values['ex_month'],
                request.values['ex_year'],
                request.values['cvv'],
                request.values['name'],
                dict_of_content['sale_token'],)
    except KeyError:
        return "400 - Missing card information"

    if is_ok:
        response = make_payment(card_info)
    else:
        logging.warning('%s is not_ok in make_sale' %(dict_of_content,))
        return str(response.status_code)

    if response.status_code != 200:
        return "Something happened<br>" + str(response.content)

    return str(response.json()["succeeded"])


@app.route('/api/sale/', methods=['GET'])
def list_sales():
    try:
        response = requests.get(
            SALE_DETAILS_URL,
            headers=HEADERS,
            auth=APIKEY_AND_SECRETKEY
        )
        results = response.json()['results']
        temp = []
        for result in results:
            temp.append({
                result.get('sale_token', 'Not Find'): {
                    'created_at': result.get('created_at', 'Not Find'),
                    'status': result.get('status', 'Not Find'),
                }
            })
    except Exception as e:
        return "Something went wrong. Please contact your business partner"
        logging.error(e)
    return jsonify(temp)


if __name__ == '__main__':
    app.run()

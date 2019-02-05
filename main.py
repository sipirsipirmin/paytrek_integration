import sqlite3
import logging
import requests
from flask import Flask, render_template
from flask import request, jsonify
from settings import SAMPLE_DATA, HEADERS, APIKEY_AND_SECRETKEY
from settings import SALE_CREATION_URL, CHARGE_URL, SALE_DETAILS_URL
from settings import DATA_TEMPLATE

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
    template = DATA_TEMPLATE
    template['customer_first_name'] = request.form.get('customer_first_name', None)
    template['customer_last_name'] = request.form['customer_last_name']
    template['billing_address'] = request.form['billing_address']
    template['billing_state'] = request.form['billing_state']
    template['billing_city'] = request.form['billing_city']
    template['billing_country'] = request.form['billing_country']
    template['customer_email'] = request.form['customer_email']

    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('''
            SELECT * FROM products;
        ''')

        list_of_all_products = cur.fetchall()
    items = []
    for name, total_amount, price in list_of_all_products:
        requested_quantity_of_product = request.form.get(name, False)
        if requested_quantity_of_product != False \
                                    and requested_quantity_of_product != u'':
            requested_quantity_of_product = int(requested_quantity_of_product)
            try:
                if requested_quantity_of_product < total_amount:
                    items.append({
                      "unit_price": price,
                      "quantity": requested_quantity_of_product,
                      "name": name,
                      "photo": "https://sandbox.paytrek.com/statics/images/testing.jpg"
                    })
            except ValueError:
                pass

    template['items'] = items

    is_ok, dict_of_content = create_sale()
    try:
        card_info = ''' {
            "number": "%s",
            "expiration": "%s/%s",
            "cvc":"%s",
            "card_holder_name":"%s",
            "sale_token":"%s"
        } ''' %(request.form['card_number'],
                request.form['ex_month'],
                request.form['ex_year'],
                request.form['cvv'],
                request.form['card_holder_name'],
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
                result.get('sale_token', 'Not Found'): {
                    'created_at': result.get('created_at', 'Not Found'),
                    'status': result.get('status', 'Not Found'),
                }
            })
    except Exception as e:
        return "Something went wrong. Please contact your business partner"
        logging.error(e)
    return jsonify(temp)


@app.route('/', methods=['GET'])
def index():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('''
            SELECT * FROM products;
        ''')
        list_of_products = cur.fetchall()
    return render_template('index.html', products=list_of_products)


if __name__ == '__main__':
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS products(name TEXT, amount INT, price FLOAT)
        ''')
        conn.commit()
    app.run()

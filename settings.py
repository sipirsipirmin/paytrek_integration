SALE_CREATION_URL = 'https://sandbox.paytrek.com/api/v2/sale/'
CHARGE_URL = 'https://sandbox.paytrek.com/api/v2/charge/'
SALE_DETAILS_URL = 'https://sandbox.paytrek.com/api/v2/sale/'
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

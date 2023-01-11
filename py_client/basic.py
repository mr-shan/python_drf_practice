import requests

from auth import get_auth_token

endpoint = "https://httpbin.org/anything"
drf_endpoint = "http://127.0.0.1:8000/api"
drf_endpoint_details = "http://127.0.0.1:8000/api/100"

# response = requests.get(drf_endpoint, data="{'key': 'value'}")
# response = requests.post(drf_endpoint, data={'key': 'value'})

post_product_data = {
    'name': 'Bold',
    'company': 'Blackberry',
    'price': '799.99'
}

filter_params = {
    'company': 'samsung'
}

auth_token = get_auth_token()

if auth_token:
    headers = { "Authorization": f"Token {auth_token}"}
    # response = requests.post(drf_endpoint, data=post_product_data)
    # response = requests.get(drf_endpoint_details)
    response = requests.get(drf_endpoint_details, params=filter_params, headers=headers)

    print(response.json())

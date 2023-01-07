import requests

endpoint = "https://httpbin.org/anything"
drf_endpoint = "http://127.0.0.1:8000/api/"

# response = requests.get(drf_endpoint, data="{'key': 'value'}")
# response = requests.post(drf_endpoint, data={'key': 'value'})

post_product_data = {
    'name': 'Bold',
    'company': 'Blackberry',
    # 'price': '799.99'
}

response = requests.post(drf_endpoint, data=post_product_data)

print(response.json())
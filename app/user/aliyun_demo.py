from uuid import uuid4
import requests

host = 'https://miitangs81.market.alicloudapi.com'
path = '/v1/tools/person/idcard'
appcode = ''
url = host + path

payload = {'idCardNo': 'miitang',
           'name': '0001'}

headers = {
    'Authorization': 'APPCODE ' + appcode,
    'X-Ca-Nonce': str(uuid4())
}

response = requests.request("POST", url, headers=headers, data=payload)
print(response.headers)
print(response.status_code)
print(response.text)

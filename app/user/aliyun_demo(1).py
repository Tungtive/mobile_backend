from uuid import uuid4
import requests

host = 'https://miitangs09.market.alicloudapi.com'
path = '/v1/tools/sms/code/sender'
appcode = ''
url = host + path

payload = {'phoneNumber': '',
           'smsSignId': '0000'}

headers = {
    'Authorization': 'APPCODE ' + appcode,
    'X-Ca-Nonce': str(uuid4())
}

response = requests.request("POST", url, headers=headers, data=payload)
print(response.headers)
print(response.status_code)
print(response.text)

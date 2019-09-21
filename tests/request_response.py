import requests
import json

url = 'https://sf-vehthft-riskmodel.herokuapp.com/'
# url= 'http://127.0.0.1:5000/'

data = {'Time': '2019-09-20 18:32:50',
        'Latitude': 37.785456,
        'Longitude': -122.470123}
j_data = json.dumps(data)
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
r = requests.post(url, data=j_data, headers=headers)
print(r, r.text)
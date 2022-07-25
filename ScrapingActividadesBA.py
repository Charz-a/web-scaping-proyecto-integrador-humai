import requests
import json


url = 'https://disfrutemosba.com/api/search'

 

payload = "{\"type_of_experiences\":[],\"kind_of_places\":[],\"min_price\":0,\"max_price\":3200,\"only_free\":0,\"dates\":[],\"moments\":[],\"districts\":[],\"only\":\"\",\"page\":1}"
headers = {'Content-Type':'application/json',
           'sec-ch-ua':'".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
           'Accept':'application/json, text/plain, */*',
           'sec-ch-ua-mobile':'?0',
           'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
           'sec-ch-ua-platform':'"Linux"'}
respuesta = requests.request("POST",url, headers=headers,data = payload)
json_response = json.loads(respuesta.text)

for beneficio in json_response['activities']['items']:
    print(beneficio['id'])
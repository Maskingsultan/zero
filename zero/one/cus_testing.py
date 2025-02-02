import requests

sando = requests.get('http://127.0.0.1:8000/cus_data/')

print(sando.status_code)
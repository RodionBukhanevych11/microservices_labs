import requests
from microservices.utils.utils import *

if __name__ == '__main__':
    url = f'http://192.168.1.49:{FACADE_PORT}/facade_service'
    messages = ['msg'+str(i) for i in range(10)]
    for text in messages:
        message = {"text":text}
        post_response = requests.post(url, json=message)
    get_response = requests.get(url)
    get_response = requests.get(url)
    get_response = requests.get(url)
    get_response = requests.get(url)

import requests
import microservices.utils.consul_utils as cf


if __name__ == '__main__':
    ports = cf.get_kv("ports")
    host = str(cf.get_kv("host")['value'])
    facade_port = str(ports["facade_port"])
    url = f'http://{host}:{facade_port}/facade_service'
    messages = ['msg'+str(i) for i in range(10)]
    for text in messages:
        message = {"text":text}
        post_response = requests.post(url, json=message)
    get_response = requests.get(url)
    get_response = requests.get(url)
    get_response = requests.get(url)
    get_response = requests.get(url)

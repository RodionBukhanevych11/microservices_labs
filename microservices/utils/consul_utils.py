from consul import Consul
import json


def put_kv(key, value):
    cons = Consul()
    cons.kv.put(key, str(value))


def get_kv(key):
    cons = Consul()
    response = cons.kv.get(key)
    value = json.loads(response[1]["Value"].decode('utf-8'))
    return value


def register_service(name, host, port, service_id=None):
    cons = Consul()
    try:
        cons.agent.service.register(name=name, service_id=service_id, address=host, port=port)
        print(f"service {name} registered")
    except Exception as e:
        print(e)


def get_service_params(service_name, service_id):
    cons = Consul()
    try:
        response = cons.catalog.service(service_name)
        service = list(filter(lambda service: service["ServiceID"]==service_id, response[1]))[0]
        host = service["ServiceAddress"]
        port = service["ServicePort"]
        return host, port
    except Exception as e:
        raise Exception('service is not found')
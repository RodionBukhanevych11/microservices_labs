import requests
from microservices.logging.logging_manager import LoggingManager
from microservices.utils.utils import *

if __name__ == '__main__':
    loggingManager = LoggingManager(LOGGERS_PORTS)
    loggingManager.run_loggers()
    url = f'http://192.168.1.49:{FACADE_PORT}/facade_service'
    messages = ['msg'+str(i) for i in range(10)]
    for text in messages:
        message = {"text":text}
        post_response = requests.post(url, json=message)
    get_response = requests.get(url)
    loggingManager.kill_loggers(2)    
    get_response = requests.get(url)       
    

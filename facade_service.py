from utils import *
from messages_service import message_client
from logging_service import Logger


class FacadeClient:
    def __init__(self, facade_port, loggers_ports, message_port):
        self._facade_client = Flask(__name__)
        self._facade_client.add_url_rule('/facade_service',view_func=self.facade_web_client_post, methods = ["POST"])
        self._facade_client.add_url_rule('/facade_service',view_func=self.facade_web_client_get, methods = ["GET"])
        self._facade_port = facade_port
        self._loggers_ports = loggers_ports
        self._message_port = message_port
        self._current_logger_port = None
        

    def run_server(self) -> bool:
        try:
            self._facade_client.run(debug=True, host='0.0.0.0', port = self._facade_port, use_reloader=False)
        except Exception as e:
            print(e)
        
        
    def get_random_logger_port(self) -> Logger:
        self._current_logger_port = random.choice(self._loggers_ports)
        
        
    def facade_web_client_post(self):
        try:
            text = str(request.get_json()['text'])
            msg = Message(text)
            self.get_random_logger_port()
            print(f"Call logger {self._current_logger_port} post method")
            log_response = requests.post(f'http://192.168.1.49:{self._current_logger_port}/log', json = msg.__dict__)
            return jsonify({"status_code":  log_response.status_code})
        except Exception as e:
            print(e)
            return jsonify({"status_code": 500})


    def facade_web_client_get(self):
        try:
            self.get_random_logger_port()
            print(f"Call logger {self._current_logger_port} get method")
            log_response = requests.get(f'http://192.168.1.49:{self._current_logger_port}/log').json()
            message_response = requests.get(f'http://192.168.1.49:{self._message_port}/message_service').json()
            print(log_response['logs'] + ', ' + message_response['message'])
            return jsonify({"status_code": 200})
        except Exception as e:
            print(e)
            return jsonify({"status_code": 500})
     
        

if __name__ == '__main__':
    facade_client = FacadeClient(FACADE_PORT, LOGGERS_PORTS, MESSAGE_PORT)
    facade_client.run_server()
    
    
    


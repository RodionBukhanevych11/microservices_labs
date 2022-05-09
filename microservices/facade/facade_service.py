from microservices.utils.utils import *
from microservices.message.messages_service import MessageClient
from microservices.logging.logging_service import Logger


class FacadeClient:
    def __init__(
            self, 
            facade_port, 
            loggers_ports, 
            messagers_ports, 
            message_broker_port, 
            queue_name
            ):
        self._facade_client = Flask(__name__)
        self._flask_thread = None
        self._facade_client.add_url_rule('/facade_service',view_func=self.facade_web_client_post, methods = ["POST"])
        self._facade_client.add_url_rule('/facade_service',view_func=self.facade_web_client_get, methods = ["GET"])
        self._facade_port = facade_port
        self._loggers_ports = loggers_ports
        self._messagers_ports = messagers_ports
        self._current_logger_port = None
        self._current_messager_port = None
        self._connection_parameters = None
        self._connection = None
        self._channel = None
        self._message_broker_port = message_broker_port
        self._queue_name = queue_name
        self.success = self.run_server()
        if self.success:
            self.run_producer()

    def run_server(self) -> bool:
        try:
            self._flask_thread = FlaskThread(target=lambda: self._facade_client.run(
                debug  = False, host = '0.0.0.0', port = self._facade_port, use_reloader = False
            ))
            self._flask_thread.start()
            print(f"Run message service port {self._facade_port}")
            return True
        except Exception as e:
            print(e)
            return False
            
            
    def run_producer(self) -> NoReturn:
        self._connection_parameters = pika.ConnectionParameters(host='0.0.0.0', 
                                                               port = self._message_broker_port
                                                               )
        self._connection = pika.BlockingConnection(self._connection_parameters)
        self._channel = self._connection.channel()
        self._channel.queue_delete(queue=self._queue_name)
        self._channel.queue_declare(queue=self._queue_name)
        
        
    def get_random_logger_port(self) -> NoReturn:
        self._current_logger_port = random.choice(self._loggers_ports)
        
        
    def get_random_messager_port(self) -> NoReturn:
        self._current_messager_port = random.choice(self._messagers_ports)
        
        
    def facade_web_client_post(self):
        text = str(request.get_json()['text'])
        msg = Message(text)
        self.get_random_logger_port()
        print(f"Call logger {self._current_logger_port} post method")
        log_response = requests.post(f'http://192.168.1.49:{self._current_logger_port}/log', json = msg.__dict__)
            
        self._channel.basic_publish(exchange='', routing_key=self._queue_name, body=msg.text)
        return jsonify({"status_code":  log_response.status_code})


    def facade_web_client_get(self):
        self.get_random_logger_port()
        print(f"Call logger {self._current_logger_port} get method")
        log_response : Dict = requests.get(f'http://192.168.1.49:{self._current_logger_port}/log').json()
            
        self.get_random_messager_port()
        print(f"Call messager {self._current_messager_port} get method")
        messager_response : Dict = requests.get(f'http://192.168.1.49:{self._current_messager_port}/message_service').json()
           
        print("LOGS = ",log_response['logs']) 
        print("MESSAGES = ",messager_response['messages'])
        return jsonify({"status_code": 200})
     

if __name__ == '__main__':
    facade_client = FacadeClient(FACADE_PORT, LOGGERS_PORTS, MESSAGERS_PORTS, MESSAGE_BROKER_PORT, QUEUE_NAME)
    
    
    
    


from utils import *


class Logger:
    def __init__(self, port: str):
        self._logging_client = Flask(__name__)
        self._logging_client.add_url_rule('/log',view_func=self.post_log, methods = ["POST"])
        self._logging_client.add_url_rule('/log',view_func=self.get_log, methods = ["GET"])
        self._port = port
        self.thread = None
        self.success = self.run_server()
        if self.success:
            self.run_client()
        

    def run_server(self) -> bool:
        try:
            self.thread = FlaskThread(target=lambda: self._logging_client.run(
                debug  = False, host = '0.0.0.0', port = self._port, use_reloader = False
            ))
            self.thread.start()
            return True
        except Exception as e:
            print(e)
            return False
            
            
    def run_client(self) -> NoReturn:
        self.hazelCastClient = hazelcast.HazelcastClient(client_name = self._port)
        self.map = self.hazelCastClient.get_map("distributed-map")
        print("len map", self.map.size().result())
        print(f'\nCreated hazelCastClient with flask server on {self._port}')
    
    
    def post_log(self) -> Dict:
        message = request.json
        print(f"flask server {self._port} received message : {message['text']}")
        self.map.put(message['uuid'],message['text'])
        return jsonify({"status_code": 200})


    def get_log(self) -> Dict:
        print(f"get request on flask server {self._port}")
        messages : List = [value for key, value in self.map.entry_set().result()]
        return jsonify({"logs":', '.join(messages),"status_code": 200})    
    
    
    def kill_thread(self) -> NoReturn:
        try:
            self.hazelCastClient.shutdown()
            self.thread.kill()
            print(f"server {self._port} killed...")
        except Exception as e:
            print(e)
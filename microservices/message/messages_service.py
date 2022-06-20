import flask
import requests
import random
from urllib import request
import hazelcast
import time
import os,sys
from typing import List, Dict, NoReturn
from flask import Flask, request, jsonify
from microservices.utils.utils import MessagerThread, Message, FlaskThread
import microservices.utils.consul_utils as cf
from typing import NoReturn

class MessageClient:
    def __init__(self, port, message_broker_port, queue_name):
        self._message_client = Flask(__name__)
        self._message_client.add_url_rule('/message_service',view_func=self.message_web_client, methods = ["GET"])
        self._port = str(port)
        self._host = str(cf.get_kv("host")['value'])
        self.flask_thread = None
        self.message_thread = None
        self.success = self.run_server()
        self._message_broker_port = str(message_broker_port)
        self._queue_name = queue_name
        self._messages_list = []
        if self.success:
            cf.register_service(name="message-service", host=self._host, port=int(self._port), service_id=f'message_{self._port}')
            self.run_consumer()
        

    def run_server(self) -> bool:
        try:
            self.flask_thread = FlaskThread(target=lambda: self._message_client.run(
                debug  = False, host = self._host, port = self._port, use_reloader = False
            ))
            self.flask_thread.start()
            print(f"Run message service port {self._port}")
            return True
        except Exception as e:
            print(e)
            return False
        
    
    def run_consumer(self) -> NoReturn:
        self.message_thread = MessagerThread(
            self._host, self._message_broker_port, self._queue_name, self._messages_list
            )
        self.message_thread.start()
            

    def message_web_client(self):
        return jsonify({"messages":', '.join(self._messages_list),"status_code": 200})    
       
    
    def kill_thread(self) -> NoReturn:
        try:
            self.thread.kill()
            print(f"server {self._port} killed...")
        except Exception as e:
            print(e)



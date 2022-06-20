import flask
import requests
import random
from urllib import request
import hazelcast
import time
import os,sys
from typing import List, Dict, NoReturn
from flask import Flask, request, jsonify
from microservices.utils.utils import FlaskThread
import microservices.utils.consul_utils as cf


class Logger:
    def __init__(self, port: str):
        self._logging_client = Flask(__name__)
        self._logging_client.add_url_rule('/log',view_func=self.post_log, methods = ["POST"])
        self._logging_client.add_url_rule('/log',view_func=self.get_log, methods = ["GET"])
        self._port = str(port)
        self._host = str(cf.get_kv("host")['value'])
        self.success = self.run_server()
        if self.success:
            self.run_client()
            cf.register_service(name="logging-service", host=self._host, port=int(self._port), service_id=f'logging_{self._port}')
        

    def run_server(self) -> bool:
        try:
            self.thread = FlaskThread(target=lambda: self._logging_client.run(
                debug  = False, host = self._host, port = self._port, use_reloader = False
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
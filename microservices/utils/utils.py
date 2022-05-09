import flask
import requests
import random
from urllib import request
import hazelcast
import time
import os,sys
from typing import List, Dict, NoReturn
from flask import Flask, request, jsonify
import threading, queue
import pika

FACADE_PORT = "8081"
LOGGERS_PORTS = ["8082","8083","8084"]
MESSAGERS_PORTS = ["8085","8086"]
MESSAGE_BROKER_PORT = "5672"
QUEUE_NAME = "mes_box"


class Message:
    _counter = 0
    def __init__(self, text):
        Message._counter += 1
        self.uuid = Message._counter
        self.text = text
        
        
class FlaskThread(threading.Thread):
    def __init__(self, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False
    def start(self):
        self.__run_backup = self.run
        self.run = self.__run     
        threading.Thread.start(self)
    def __run(self):
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup
    def globaltrace(self, frame, why, arg):
        if why == 'call':
          return self.localtrace
        else:
          return None
    def localtrace(self, frame, why, arg):
        if self.killed:
          if why == 'line':
            raise SystemExit()
        return self.localtrace
    def kill(self):
        self.killed = True
    
    
class MessagerThread(threading.Thread):
    def __init__(self, port : str, queue_name : str, messages_list : List):
        super(MessagerThread, self).__init__()
        self._is_interrupted = False
        self._port = port
        self._queue_name = queue_name
        self.messages_list = messages_list

    def stop(self):
        self._is_interrupted = True

    def run(self):
        connection_parameters = pika.ConnectionParameters(host = '0.0.0.0', 
                                                          port = self._port
                                                          )
        connection = pika.BlockingConnection()
        channel = connection.channel()
        channel.queue_declare(queue = self._queue_name, durable = False)
        channel.basic_qos(prefetch_count=1)
        for message in channel.consume(self._queue_name, auto_ack = True):
            if self._is_interrupted:
                break
            if not message:
                continue
            method, properties, body = message
            if body is not None:
                self.messages_list.append(body.decode("utf-8"))


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
from microservices.message.messages_service import MessageClient
import microservices.utils.consul_utils as cf
from typing import NoReturn

class MessagesManager:
    def __init__(self):
        ports = cf.get_kv("ports")
        self.messager_ports = ports["messagers_ports"]
        self.message_broker_port = ports["message_broker_port"]
        self.queue_name = cf.get_kv("queue_name")['name']
        
        
    def run(self) -> NoReturn:
        for port in self.messager_ports:
            messager = MessageClient(port, self.message_broker_port, self.queue_name)
       

if __name__ == '__main__':
    messagesManager = MessagesManager()
    messagesManager.run()
import flask
import requests
import random
from urllib import request
import hazelcast
import random
import time
import os,sys
from typing import List, Dict, NoReturn
from flask import Flask, request, jsonify
import threading

FACADE_PORT = "8081"
LOGGERS_PORTS = ["8083","8084","8085"]
MESSAGE_PORT = "8082"


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


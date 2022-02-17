import flask
from flask import Flask, request, jsonify


class Message:
    _counter = 0
    def __init__(self, text):
        Message._counter += 1
        self.uuid = Message._counter
        self.text = text


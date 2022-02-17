from urllib import request
from app import *
import requests
from logging_service import logger
from messages_service import message_client

facade_client = Flask(__name__)

@facade_client.route('/facade_service', methods=['POST'])
def facade_web_client_post():
    try:
        text = str(request.get_json()['text'])
        msg = Message(text)
        log_response = requests.post('http://192.168.1.49:8081/log', json = msg.__dict__)

        if log_response.status_code == 200:
            return jsonify({"status_code": 200})
        else:
            return jsonify({"status_code": 500})

    except:
        return jsonify({"status_code": 500})

@facade_client.route('/facade_service', methods=['GET'])
def facade_web_client_get():
    try:
        log_response = requests.get('http://192.168.1.49:8081/log').json()
        message_response = requests.get('http://192.168.1.49:8082/message_service').json()
        print(log_response['logs'] + ', ' + message_response['message'])

        return jsonify({"status_code": 200})
        
    except:
        return jsonify({"status_code": 500})


if __name__ == '__main__':
    facade_client.run(debug=True, host='0.0.0.0', port = '8080')
    


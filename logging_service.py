from app import *


class Logger:
    def __init__(self):
        self.log_dict = dict()
        self.logging_client = Flask(__name__)

logger = Logger()

@logger.logging_client.route('/log', methods=['POST'])
def log():
    message = request.json
    print(message['text'])
    try:
        logger.log_dict.update({message['uuid']:message['text']})
    except:
        print('Not Message object!')

    return jsonify({"status_code": 200})                 

@logger.logging_client.route('/log', methods=['GET'])
def get_logs():
    return jsonify({"logs":', '.join(list(logger.log_dict.values())),"status_code": 200})    

if __name__ == '__main__':
    logger.logging_client.run(debug=True, host='0.0.0.0', port = '8081')

            
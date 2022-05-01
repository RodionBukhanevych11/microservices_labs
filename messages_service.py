from utils import *


message_client = Flask(__name__)

@message_client.route('/message_service', methods=['GET'])
def message_web_client():
    return jsonify({"message":'not implemented yet',"status_code": 200})


if __name__ == '__main__':
    message_client.run(debug=True, host='0.0.0.0', port = MESSAGE_PORT)
    


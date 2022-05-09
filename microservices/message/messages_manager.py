from microservices.utils.utils import *
from microservices.message.messages_service import MessageClient


class MessagesManager:
    def __init__(self, ports, message_broker_port, queue_name):
        self.messager_ports = ports
        self.message_broker_port = message_broker_port
        self.queue_name = queue_name

        
    def run(self) -> NoReturn:
        for port in self.messager_ports:
            messager = MessageClient(port, self.message_broker_port, self.queue_name)
       

if __name__ == '__main__':
    messagesManager = MessagesManager(MESSAGERS_PORTS,MESSAGE_BROKER_PORT,QUEUE_NAME)
    messagesManager.run()
from microservices.utils.utils import *
from microservices.logging.logging_service import Logger
import microservices.utils.consul_utils as cf


class LoggingManager:
    def __init__(self):
        ports = cf.get_kv("ports")
        self.loggers_ports = ports["loggers_ports"]
        self.active_loggers = []
        
    def run(self) -> NoReturn:
        print(self.loggers_ports)
        for port in self.loggers_ports:
            logger = Logger(port)
            if logger.success:
                self.active_loggers.append(logger)
                
       
    def kill(self,n) -> NoReturn:
        shutdown_loggers : List[Logger] = random.sample(self.active_loggers, 2)
        for logger in shutdown_loggers:
            logger.kill_thread()
                

if __name__ == '__main__':
    loggingManager = LoggingManager()
    loggingManager.run()
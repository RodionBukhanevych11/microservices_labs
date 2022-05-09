from microservices.utils.utils import *
from microservices.logging.logging_service import Logger


class LoggingManager:
    def __init__(self, ports):
        self.loggers_ports = ports
        self.active_loggers = []

        
    def run(self) -> NoReturn:
        for port in self.loggers_ports:
            logger = Logger(port)
            if logger.success:
                self.active_loggers.append(logger)
       
    def kill(self,n) -> NoReturn:
        shutdown_loggers : List[Logger] = random.sample(self.active_loggers, 2)
        for logger in shutdown_loggers:
            logger.kill_thread()
                

if __name__ == '__main__':
    loggingManager = LoggingManager(LOGGERS_PORTS)
    loggingManager.run()
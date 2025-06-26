from abc import ABC, abstractmethod
import logging

class BaseAgent(ABC):
    def __init__(self, name):
        self.name = name
        self.logger = logging.getLogger(name)
        logging.basicConfig(level=logging.INFO)
        
    @abstractmethod
    def execute(self, *args, **kwargs):
        pass
    
    def log_action(self, message):
        self.logger.info(f"[{self.name}] {message}")
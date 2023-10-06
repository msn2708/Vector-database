import logging.config
import threading
from get_config import Config
import ruamel.yaml as yaml

# This class reads the configuration file and creates 
# a logger for each configuration it encounters in the config file.
# The getLogger method will then return the logger by name if it exists.
class Loggers:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(Loggers, cls).__new__(cls)
                cls._instance._configure_loggers()                
            return cls._instance
        
    def _configure_loggers(self):
        self.myloggers = {}    
        try:
            with open('logging.yml', 'r') as config_file:
                log_config = yaml.safe_load(config_file)
                logging.config.dictConfig(log_config)
                for logger_item in log_config['loggers']:
                    try:                                    
                        self.myloggers[logger_item] = logging.getLogger(log_config.get(logger_item))
                    except Exception as e:
                        print(f"Error configuring logger '{logger_item}': {e}")  
                self.logger = logging.getLogger(log_config.get('logger_name', 'default_logger'))
        except FileNotFoundError:
            print("Error: Configuration file logging.yml not found.")
            raise
        except Exception as e:
            print(f"Error: Unable to configure logger: {e}")
            raise
    
    def get_logger(self, logger_name):
        if logger_name in self.myloggers:
            return self.myloggers.get(logger_name)
        else:
            raise KeyError(f"Logger '{logger_name}' is not defined in the configuration.")


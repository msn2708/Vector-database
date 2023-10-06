import ruamel.yaml as yaml
import threading

class Config:
    _instance = None
    _config = None
    _lock = threading.Lock()  # Create a lock for thread safety

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:  # Acquire the lock before creating an instance
                if cls._instance is None:
                    cls._instance = super(Config, cls).__new__(cls)
                    cls._instance.load_config()
        return cls._instance

    def load_config(self):
        try:
            with open('config.yml') as config_file:
                self._config = yaml.safe_load(config_file)
        except FileNotFoundError as e:
            print(f"The config.yml file was not found {e}")
            raise SystemExit(-1)

    def get_config(self):
        if self._config is None:
            with self._lock:  # Acquire the lock before loading the config
                if self._config is None:
                    self.load_config()
        return self._config


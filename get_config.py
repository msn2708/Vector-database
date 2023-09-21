import yaml

class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._config = None
            cls._instance.load_config()
        return cls._instance

    def load_config(self):
        try:
            with open('config.yml') as config_file:
                self._config = yaml.safe_load(config_file)
        except FileNotFoundError:
            print("No configuration file config.yml found")
            raise SystemExit(-1)

    def get_config(self):
        if self._config is None:
            self.load_config()
        return self._config

# Usage:
# Create an instance of Config
#config_instance = Config()

# Access the configuration
#config = config_instance.get_config()

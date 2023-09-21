import yaml

def get_config():   
    try: 
        with open('config.yml') as config_file:
            config=yaml.safe_load(config_file)
            return config    
    except FileNotFoundError:
        print("No configuration file found")
        raise SystemExit(-1)
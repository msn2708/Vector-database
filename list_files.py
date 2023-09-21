import os
from confluent_kafka import Producer, Consumer, KafkaError
from get_config import Config

def list_files():
    #write each file to a kafka topic
    try:
        config = Config().get_config()
        data_dir = config.get('data_dir')     
        producer = Producer(config.get('producer'))
        for root,_,files in os.walk(data_dir):
            for file in files: 
                producer.produce(config.get('kafka-topic'), key=file, value=os.path.join(root, file))
                producer.flush()
        #return [os.path.join(root, file) for root, _, files in os.walk(data_dir) for file in files]
    except Exception as e: 
        print(f"Error in listing the directory: {e}")
    except KeyboardInterrupt:
        pass
    
    finally:
        producer.flush()
        
if __name__ == '__main__':
    list_files()
import os
from confluent_kafka import Producer, Consumer, KafkaError
from get_config import get_config

def list_files(dir):
    #write each file to a kafka topic
    try:
        config = get_config()
        data_dir = config.get('data_dir')     
        producer = Producer(config.get('producer'))
        for root,_,files in os.walk(data_dir):
            for file in files: 
                producer.produce('tp-list-files', key=file, value=os.path.join(root, file))
                producer.flush()
        #return [os.path.join(root, file) for root, _, files in os.walk(data_dir) for file in files]
    except Exception as e: 
        print(f"Error in listing the directory: {e}")
    except KeyboardInterrupt:
        pass
    
    finally:
        producer.flush()
        
if __name__ == '__main__':
    files = list_files("/Users/smohammed/Documents/GitHub/Code/Support Vectors")
    for file in files:
        print (file) 
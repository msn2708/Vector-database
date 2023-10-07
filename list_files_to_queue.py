import os
from confluent_kafka import Producer
from get_config import Config
from initlog import Loggers

def list_files_to_queue():
    #write each file to a kafka topic
    try:
        config = Config().get_config()
        data_dir = config['corpus']['data_dir']   
        producer = Producer(config.get('producer'))
        topic = config.get('kafka-topic')

        loggers = Loggers()
        logger = loggers.get_logger(logger_name='text-processing')
        
        for root,_,files in os.walk(data_dir):
            for file in files:                
                producer.produce(topic, key=file, value=os.path.join(root, file))
                logger.info(f"Listed file {file.decode('utf-8')} to queue {topic} ")
                producer.flush()
    except Exception as e: 
            logger.error (f"Error in listing the directory: {e}")
    except KeyboardInterrupt:
        pass
    
    finally:
        producer.flush()
        
if __name__ == '__main__':
    list_files_to_queue()
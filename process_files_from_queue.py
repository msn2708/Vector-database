import os
from get_config import Config
from confluent_kafka import Consumer, KafkaError
from process_file import process_file
from initlog import Loggers


def process_files_from_queue():
    #read a file from kafka topic
    try:
        config = Config().get_config()
        consumer = Consumer(config.get('consumer'),enable_auto_commit=False)
        consumer.subscribe([config.get('kafka-topic')])
        logger = Loggers().get_logger('text-processing')
                
        while True:
            message = consumer.poll(1.0)
            consumer.commit()
            
            if message is None:
                continue

            if message.error():
                if message.error().code() == KafkaError._PARTITION_EOF:
                    logger.info ('process_files_from_queue: Reached the end of partition while processing files')
                else:
                    logger.error (f'process_files_from_queue: Error: {message.error().str()}')
            else:
                try:
                    key = message.key().decode('utf-8')
                    value = message.value().decode('utf-8')
                    
                    logger.info (f'process_files_from_queue: Consumed message: key={key}, value={value}')
                    process_file(value)
                    
                except Exception as e:
                    logger.exception(f"process_files_from_queue: Exception encountered when processing {message.key()}")                    
                    continue
                finally:
                    logger.info (f"process_files_from_queue: Successfully proceessed file {message.key()}")                    
    except Exception:
        pass

    finally:
        consumer.close()
        
if __name__ == '__main__':
    process_files_from_queue()
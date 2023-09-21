import os
from get_config import Config
from confluent_kafka import Producer, Consumer, KafkaError
from process_file import process_file

def process_pdf_files_from_queue():
    #read a file from kafka topic
    try:
        config = Config().get_config()
        consumer = Consumer(config.get('consumer'))
        consumer.subscribe(config.get('kafka-topic'))
        
        while True:
            message = consumer.poll(1.0)

            if message is None:
                continue

            if message.error():
                if message.error().code() == KafkaError._PARTITION_EOF:
                    print('Reached end of partition')
                else:
                    print(f'Error: {message.error().str()}')
            else:
                print(f'Consumed message: key={message.key()}, value={message.value()}')
                #process the file
                process_file(message.value())                                

    except KeyboardInterrupt:
        pass

    finally:
        consumer.close()
        
if __name__ == '__main__':
    process_pdf_files_from_queue()
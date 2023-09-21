import os
from get_config import get_config
from confluent_kafka import Producer, Consumer, KafkaError
from process_file import process_file

def process_pdf_files_from_queue():
    #read a file from kafka topic
    try:
        config = get_config()
        consumer = Consumer(config.get('pdf_config'))
        consumer.subscribe(config.get('pdf_files'))
        
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
    files = list_files("/Users/smohammed/Documents/GitHub/Code/Support Vectors")
    for file in files:
        print (file) 
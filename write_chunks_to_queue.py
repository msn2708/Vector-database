from confluent_kafka import Producer
from get_config import Config

def write_chunks_to_queue(chunk):
    try:
        producer = Producer(Config().get_config().get('embedding-producer'))
        producer.produce(Config().get_config().get('kafka-embedding-topic'), key=chunk.chunk_id & '_' & chunk.document_id, value=chunk.embedding)
        producer.flush()
    except Exception as e: 
        print(f"Error in writing embedding to kafka-embedding-topic: {e.with_traceback()}")
    except KeyboardInterrupt:
        pass
        
    finally:
        producer.flush()
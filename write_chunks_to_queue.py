from confluent_kafka import Producer
from get_config import Config
from initlog import Loggers

def write_chunks_to_queue(chunk):
    try:
        loggers = Loggers()
        logger = loggers.get_logger(logger_name='text-processing')
        
        producer = Producer(Config().get_config().get('embedding-producer'))        
        producer.produce(Config().get_config().get('kafka-embedding-topic'), key=str(chunk.chunk_id).encode('utf-8'), value=chunk.embedding)
        logger.info(f"Successfully wrote {str(chunk.chunk_id)} to the queue")
        producer.flush()
    except Exception as e: 
        logger.error (f"Error in writing embedding to kafka-embedding-topic: {e.with_traceback()}")
    except KeyboardInterrupt:
        pass
        
    finally:
        producer.flush()
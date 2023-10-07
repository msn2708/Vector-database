from confluent_kafka import Consumer, KafkaException
import faiss
import numpy as np
import json
from get_config import Config

config = Config().get_config()

# Kafka consumer
consumer = Consumer(config.get('embedding-consumer'))

# FAISS index configuration
dimension =  768
nlist = 100
index = faiss.IndexFlatIP(dimension)  # Cosine similarity (dot product similarity) index

# FAISS index configuration
# dimension = 768
# connections = 64
# search_layers = 32
# build_layers = 64
# index = faiss.IndexHNSWFlat(dimension,connections)
# index.hnsw.efConstruction = build_layers
# index.hnsw.efSearch = search_layers


# Subscribe to the Kafka topic
topics = ['tp-vector-embedding']
consumer.subscribe(topics)

try:
    while True:
        msg = consumer.poll(1.0)  # 1-second timeout for polling messages

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaException._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break

        # Decode message value from JSON
        try:
            chunk_id = msg.key().decode('utf-8')
            vector_embedding = np.frombuffer(msg.value(),dtype=np.float32)
            
            # Add vector embedding to the FAISS index
            index.add(np.expand_dims(vector_embedding, axis=0))
            print(f"Added vector embedding for chunk_id {chunk_id} to the FAISS index.")
        except Exception as e:
            print(f"Error processing message: {e}")

except KeyboardInterrupt:
    pass
finally:
    # Close down consumer to commit final offsets.
    consumer.close()

# Optionally, you can save the index to disk for later use
faiss.write_index(index, "cosine_similarity_index.faiss")

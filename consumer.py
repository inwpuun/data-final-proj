from kafka import KafkaConsumer
import pandas as pd

kafka_broker = 'localhost:9092'

consumer = KafkaConsumer(
    'sample',
    bootstrap_servers=[kafka_broker],
    enable_auto_commit=True,
    value_deserializer=lambda x: x.decode('utf-8'))

print('Running Consumer')

for message in consumer:
    print(message)
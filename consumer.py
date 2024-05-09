from kafka import KafkaConsumer
import csv
import json


kafka_broker = 'localhost:9092'

consumer = KafkaConsumer(
    'sample',
    bootstrap_servers=[kafka_broker],
    enable_auto_commit=True,
    value_deserializer=lambda x: x.decode('utf-8'))

print('Running Consumer')

csv_file_path = 'output.csv'
field_names = ["Title", "Affiliation", "Subject", "Year", "Source_Id", "Citedby_Count"]

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_names, delimiter=';')
    writer.writeheader()
    for message in consumer:
        print(message.offset)
        writer.writerow(json.loads(message.value))
    
consumer.close()
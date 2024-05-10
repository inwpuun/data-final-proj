from kafka import KafkaConsumer
import csv
import json

print('Running Consumer')

consumer = KafkaConsumer(
    'scopus',
    bootstrap_servers='kafka:9092',
    enable_auto_commit=True,
    value_deserializer=lambda x: x.decode('utf-8'))

csv_file_path = '/app/out/scopus_data1.csv'
field_names = ["Title", "Affiliation", "Subject", "Year", "Source_Id", "Citedby_Count"]

with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_names, delimiter=';')
    try:
        while True:
            msg = consumer.poll(0.1)
            if msg is None or msg == {}:
                continue
            print(json.loads(list(msg.values())[0][0].value))
            writer.writerow(json.loads(list(msg.values())[0][0].value))
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
    
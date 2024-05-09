from kafka import KafkaConsumer
import pandas as pd
import csv
import json
import shutil

kafka_broker = 'kafka:9092'
print('Running Consumer')

consumer = KafkaConsumer(
    'scopus',
    bootstrap_servers=kafka_broker,
    enable_auto_commit=True,
    value_deserializer=lambda x: x.decode('utf-8'))


csv_file_path = '/app/out/scopus_data.csv'
field_names = ["Title", "Affiliation", "Subject", "Year", "Source_Id", "Citedby_Count"]
# shutil.copyfile("/app/output.csv", csv_file_path)

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_names, delimiter=';')
    try:
        print('ahhhh shit')
        while True:
            msg = consumer.poll(0.1)
            print('this', msg)
            if msg is None or msg == {}:
                continue
            print(list(msg.values())[0][0].value)
            writer.writerow(json.loads(list(msg.values())[0][0].value))
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
    
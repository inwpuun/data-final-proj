from kafka import KafkaProducer

import time
import json
import os

kafka_broker = 'localhost:9092'

producer = KafkaProducer(bootstrap_servers=[kafka_broker])

folder_path = "./Data_2018-2023"
year_lists = os.listdir(folder_path)

def read_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def extract_data(json_data):
    # Extract only the required data from the JSON
    item = json_data['abstracts-retrieval-response']
    extracted_data = {
        'affiliation': item['affiliation'], 
        'title': item['coredata']['dc:title'],
        'cover-date': item['coredata']['prism:coverDate'],
        'citedby-count' : item['coredata']['citedby-count'],
        'source-id' : item['coredata']['source-id'],
        'subject-areas': item['subject-areas']
    }
    
    return extracted_data

for i in year_lists:
    path = folder_path + '/' + i
    files = os.listdir(path)
    for j in files:
        file_path = path + '/' + j
        data = read_file(file_path)
        extracted_data = extract_data(data)
        producer.send('sample', json.dumps(extracted_data).encode('utf-8'))
        time.sleep(1)


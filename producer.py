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

def mapped_affiliation(affiliation) :
    if isinstance(affiliation, list) :
        return [{'affilname': entry['affilname'].replace(';', '|'), 'affiliation-city': entry['affiliation-city'], 'affiliation-country': entry['affiliation-country']} for entry in affiliation]
    return [{'affilname': affiliation['affilname'].replace(';', '|'), 'affiliation-city': affiliation['affiliation-city'], 'affiliation-country': affiliation['affiliation-country']}]

def map_int(i) :
    if i is not None and i.isnumeric() :
        return int(i)
    return 0

def map_year(y) :
    if y is not None and isinstance(y, str) :
        return y.split('-')[0]
    return -1

def extract_data(json_data):
    # Extract only the required data from the JSON
    item = json_data['abstracts-retrieval-response']
    if 'dc:title' not in item['coredata'] or 'affiliation' not in item:
        return None
    extracted_data = {
        'Title': item['coredata']['dc:title'].replace(';', '|'),
        'Affiliation': mapped_affiliation(item['affiliation']), 
        'Subject': [entry['@abbrev'].replace(';', '|') for entry in item['subject-areas']['subject-area']],
        'Year': map_year(item['coredata']['prism:coverDate']),
        'Source_Id' : item['coredata']['source-id'],
        'Citedby_Count' : map_int(item['coredata']['citedby-count']),
    }
    
    return extracted_data

for i in year_lists:
    path = folder_path + '/' + i
    print(path)
    if (path == './Data_2018-2023/.DS_Store') :
        continue
    
    files = os.listdir(path)
    for j in files:
        file_path = path + '/' + j
        print(file_path)
        data = read_file(file_path)
        extracted_data = extract_data(data)
        if extract_data is None :
            continue
        producer.send('star', json.dumps(extracted_data).encode('utf-8'))
        # time.sleep(1)




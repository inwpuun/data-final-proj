import requests
import pandas as pd
from kafka import KafkaProducer
import json
import csv
import os

SCOPUSPOINTER = "scopusPointer1.csv"

def start_kafka_producer():
    producer = KafkaProducer(bootstrap_servers='kafka:9092')
    return producer

def read_start_pointer() :
    print("isExist", os.path.exists(SCOPUSPOINTER))
    if not os.path.exists(SCOPUSPOINTER):
        subjects = ["GENE","AGRI","ARTS","BIOC","BUSI","CENG","CHEM","COMP","DECI","EART","ECON","ENER","ENGI","ENVI","IMMU","MATE","MATH","MEDI","NEUR","NURS","PHAR","PHYS","PSYC","SOCI","VETE","DENT","HEAL"] #27 subjects
        years = ['2018','2019','2020','2021','2022','2023']
        with open(SCOPUSPOINTER, 'w', newline='') as file:
            for a in years :
                for b in subjects :
                    file.write(f'{a}, {b}, 0\n')
    result = {}
    with open(SCOPUSPOINTER, newline='') as file:
        csv_reader = list(csv.reader(file, delimiter=","))
        for row in csv_reader:
            result[f'{row[0].strip()}{row[1].strip()}'] = int(row[2].strip())
    return result

def write_start_pointer(result) :
    with open(SCOPUSPOINTER, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        for pointer in result :    
            csv_writer.writerows([pointer[0], pointer[1], result[pointer]])

def mapped_affiliation(affiliation) :
    if isinstance(affiliation, list) :
        return [{'affilname': entry['affilname'].replace(';', '|'), 'affiliation-city': entry['affiliation-city'], 'affiliation-country': entry['affiliation-country']} for entry in affiliation]
    return [{'affilname': affiliation['affilname'].replace(';', '|'), 'affiliation-city': affiliation['affiliation-city'], 'affiliation-country': affiliation['affiliation-country']}]

def map_int(i) :
    if i is not None and i.isnumeric() :
        return int(i)
    return 0

def get_scopus_data():
    api_key = 'd9ce26eb81f254add03b327aef475678'
    base_url = 'https://api.elsevier.com/content/search/scopus'
    count = 25
    subjects = ["GENE","AGRI","ARTS","BIOC","BUSI","CENG","CHEM","COMP","DECI","EART","ECON","ENER","ENGI","ENVI","IMMU","MATE","MATH","MEDI","NEUR","NURS","PHAR","PHYS","PSYC","SOCI","VETE","DENT","HEAL"] #27 subjects
    years = ['2018','2019','2020','2021','2022','2023']
    
    producer = start_kafka_producer()
    start_pointer = read_start_pointer()
    for year in years :
        for subj in subjects :
            print('year', year, 'subject', subj)
            query = f'AFFIL(chulalongkorn university) AND subjarea(${subj}) AND PUBYEAR > ${int(year) - 1} AND PUBYEAR < ${int(year) + 1}'
            start = start_pointer[f'{year}{subj}']
            while True : 
                response = requests.get(f'{base_url}?apiKey={api_key}&query={query}&start={start}')
                data = response.json()
                reach5000 = False
                
                if 'search-results' not in data:
                    break
                
                if(int(data['search-results']['opensearch:totalResults']) < start):
                    break
                
                if 'entry' in data['search-results']:
                    for entry in data['search-results']['entry']:
                        if 'error' in entry :
                            continue
                        
                        title = entry.get('dc:title', None)
                        affi = entry.get('affiliation', None)
                        sourceId = entry.get('source-id', None)
                        citedCount = entry.get('citedby-count', None)

                        if title is not None and affi is not None and sourceId is not None and citedCount is not None:
                            data = {'Title': title, 
                                    'Affiliation': mapped_affiliation(affi), 
                                    'Source_Id' : sourceId, 
                                    'Subject': [subj], 
                                    'Year': year, 
                                    "Citedby_Count" : map_int(citedCount)
                                }
                            print(data['Source_Id'])
                            producer.send('scopus', json.dumps(data).encode('utf-8'))
                        if start >= 5000 : 
                            reach5000 = True
                            break
                        # time.sleep(0.1)
                start += count
                if reach5000 :
                    break
            start_pointer[f'{year}{subj}'] = start
    write_start_pointer(start_pointer)

        
#     # for pointer in result :    
# get_scopus_data()
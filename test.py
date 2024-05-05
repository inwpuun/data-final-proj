import requests
import pandas as pd
api_key = 'd9ce26eb81f254add03b327aef475678'
base_url = 'https://api.elsevier.com/content/search/scopus'
query = 'AFFIL(chulalongkorn university) AND subjarea(COMP) AND PUBYEAR > 2018'
count = 25
start = 0
results = []
maxData = 5
df = pd.DataFrame(columns=['Title', 'Affiliation', 'Subject','Year'])

subjects = ["GENE","AGRI","ARTS","BIOC","BUSI","CENG","CHEM","COMP","DECI","EART","ECON","ENER","ENGI","ENVI","IMMU","MATE","MATH","MEDI","NEUR","NURS","PHAR","PHYS","PSYC","SOCI","VETE","DENT","HEAL"] #27 subjects

years = ['2018','2019','2020','2021','2022','2023',]



query = 'AFFIL(chulalongkorn university) AND subjarea(COMP) AND PUBYEAR(2018)'
url = f'{base_url}?apiKey={api_key}&query={query}&count={count}&start={start}'
response = requests.get(url)
data = response.json()
print(data)
if 'search-results' in data:
    total_results = int(data['search-results']['opensearch:totalResults'])
    current_results = int(data['search-results']['opensearch:itemsPerPage'])
    entry = data['search-results']['entry']
    title = entry[0]['dc:title']
    affi = entry[0]['affiliation']
    print(title,affi)
    df = df.append({'Title': title, 'Affiliation': affi, 'Subject': "COMP", 'Year' : "2018" }, ignore_index=True)
    
print(df)
df.to_csv("dataTest.csv", index=False)
# start += count
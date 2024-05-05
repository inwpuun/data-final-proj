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



for year in years :
    for subj in subjects :
        query = 'AFFIL(chulalongkorn university) AND subjarea({'+ subj +'}) AND PUBYEAR({'+year+'})'
        url = f'{base_url}?apiKey={api_key}&query={query}&count={count}&start={start}'
        response = requests.get(url)
        data = response.json()

        if 'search-results' in data:
            total_results = int(data['search-results']['opensearch:totalResults'])
            current_results = int(data['search-results']['opensearch:itemsPerPage'])
            entry = data['search-results']['entry']
            title = entry[0]['dc:title']
            affi = entry[0]['affiliation']
            print((title,affi,year,subj))
            
            # results.append((title,affi,year,subj))
            # print(title,affi)
            # df = df.append({'Title': title, 'Affiliation': affi, 'Subject': subj, 'Year' : year }, ignore_index=True)
            
        
        # start += count


# for year in years :
#     for subj in subjects :
        # df = pd.DataFrame(columns=['Title', 'Affiliation', 'Subject','Year'])
        # while True:
        #     query = 'AFFIL(chulalongkorn university) AND subjarea({subj}) AND PUBYEAR({year})'
        #     url = f'{base_url}?apiKey={api_key}&query={query}&count={count}&start={start}'
        #     response = requests.get(url)
        #     data = response.json()
            
        #     if 'search-results' in data:
        #         total_results = int(data['search-results']['opensearch:totalResults'])
        #         current_results = int(data['search-results']['opensearch:itemsPerPage'])
        #         results.extend(data['search-results']['entry'])
        #         for entry in data['search-results']['entry']:
        #             title = entry['dc:title']
        #             affi = entry['affiliation']

        #             df = df.append({'Title': title, 'Affiliation': affi, 'Subject': subj, 'Year' : year }, ignore_index=True)
                    
        #         if current_results < count or start + current_results >= total_results or len(df) >= maxData:
        #             break
                
        #         start += count
        #     else:
        #         break
        # df

    

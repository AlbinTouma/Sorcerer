import pandas as pd
import numpy as np
import os
from tabulate import tabulate

# Load Data
input_directory = '../src/parquet/'
input_files = [f for f in os.listdir(input_directory) if f.endswith('.parquet')]
list_df = []
for input_file in input_files:
    input_file_path = os.path.join(input_directory, input_file)
    data = pd.read_parquet(input_file_path)
    list_df.append(data)

data = pd.concat(list_df).reset_index(drop=True)
data = data.where(pd.notnull(data), None)

#Prepare data
data['_source.sources.source_ids'] = data['_source.sources.source_ids'].apply(lambda x: ', '.join(map(str, x)))
data['completeness'] = data['completeness'].replace(0, 'incomplete')

# Select Sources
LIST_SOURCE_SOURCE_IDS = ['S:FBFYW0 [DBPedia]','S:4CU7GM [PEP Everypolitician]', 'S:8L276A [Manual PEPs]', 'S:1GYJGG [The Official Board]', 'S:MFCNUA [PEP US Diplomat list 2]']
data = data[data['_source.sources.source_ids'].isin(LIST_SOURCE_SOURCE_IDS)]

#Remove RCAs
RCA_DBPEDIA = data[(data['_source.sources.source_ids'] == 'S:FBFYW0 [DBPedia]') & (data['PEP_id'] == False)]
data.drop(RCA_DBPEDIA.index, inplace=True)


#Check if name is valid by looking at TOTAL FLAGS > 0. Zero for invalid names and 1 for valid. There are no Null values here
name_check = data['TOTAL_FLAGS'].apply(lambda x: 0 if x > 0 else 1)
#Birth date (Good enough = valid, t1 - t3 must have the field). Zero if empty or >200 otherwise 1
date_of_birth = data['_source.data.births.age'].apply(lambda x: None if pd.isna(x) else (0 if x >= 200 else 1))
#Date of death. None if None, 1 if <= 100 else 0.
date_of_death = data['_source.data.deaths.years_since_death'].apply(lambda x: None if x is pd.isna(x) or np.nan else (1 if x <=100 else 0))
#Extracted relevant pep occupation from display.value and occupation fields so checking for None values is not possible.
occupation = data['has_occupation'].apply(lambda x: 0 if x == False else 1)
#Location check. If None return none. If all values a continent then return 0, else 1. This value is a list of places [] so iterate through each list for each row. 
data['source.data.locations.name'] = data['_source.data.locations.name'].apply(lambda x: x.tolist() if x is not None else None) #Convert np.array to list for each row in pd.Series
continents = ['North America', 'South America', 'Europe', 'Asia', 'Africa', 'Oceania', 'Middle East']
location = data['source.data.locations.name'].apply(lambda x: None if x is None else (0 if all(value in continents for value in x) else 1))
# Source url. None for None values, 0 if all in list invalid url and 1 if valid url 
data['_source.assets.external_urls'] = data['_source.assets.external_urls'].apply(lambda x: x.tolist() if x is not None else None)
reject_urls = ['http://complyadvantage.com','https://complyadvantage.com']
source_url = data['_source.assets.external_urls'].apply(lambda x: None if x is None else (0 if all(url in reject_urls for url in x) else 1))
#PEP start date
start_date = data['_source.data.aml_types.start_date'].apply(lambda x: None if all(date is None for date in x) else 1)


result = pd.DataFrame({
    "name": name_check,
    "dob": date_of_birth,
    "dod": date_of_death,
    "occupation": occupation,
    "location": location,
    "source url": source_url, 
    "start date": start_date,
    })

result['tier'] = None
#Reject all with invalid names
result.loc[(name_check == 0) | (date_of_birth == 0) | (date_of_death == 0) | (occupation == 0) | (location == 0), 'tier'] = 'Reject'
result.loc[(date_of_birth == None) | (date_of_death == None) | (location == None), 'tier'] = 'Insufficient'
print(result['tier'].value_counts())

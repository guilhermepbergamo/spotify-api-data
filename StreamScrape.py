import os
import json
import pandas as pd


files = os.listdir()
json_files = []
all_names = {'Track Name':[], 'Streams':[]}
   
for file in files:
    if file.endswith('.txt'):
        json_files.append(file)

print(json_files)

for json_file in json_files:

    with open(json_file, mode='r', encoding='cp932', errors='ignore') as file:
        json_data = json.load(file)

    content = json_data['data']['playlistV2']['content']
    items = content['items']
    playcounts = []
    names = []

    for item in items:
        playcount = item['itemV2']['data']['playcount']
        name = item['itemV2']['data']['name']
        names.append(name)
        playcounts.append(playcount)

    all_names['Streams'].extend(playcounts)
    all_names['Track Name'].extend(names)

dataframe = pd.read_csv('mostpopularsongsalltime.csv')
dataframe2 = pd.DataFrame(all_names)

#total_linhas = len(dataframe2)
#print(total_linhas)
#dataframe2 = dataframe2.iloc[:total_linhas - 33, :]

df_final = pd.merge(dataframe, dataframe2, on='Track Name', how='inner')

#dataframe['Streams'] = dataframe2['Streams']
df_final.to_csv('teste.csv')

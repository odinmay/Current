import json
import os

master_list = []
path = os.getcwd()
with open(path + '/cah-cards-full.json', encoding='utf-8') as f:
    data = json.load(f)
    for outer_dict in data:
        counter = 0
        for dict in data[str(counter)]['black']:
            master_list.append(dict.get('text'))


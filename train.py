import os
import json
import pandas as pd
import numpy as np

disaster_key_dict = {}

df = pd.read_csv('train.csv')
for index, row in df.iterrows():
	if row['Label'] not in disaster_key_dict:
		disaster_key_dict[row['Label']] = set()
	if type(row['Tweet']) != str or type(row['Label']) != str:
		continue
	disaster_key_dict[row['Label']] = disaster_key_dict[row['Label']].union(set(row['Tweet'].split()))

for key in disaster_key_dict:
	disaster_key_dict[key] = list(disaster_key_dict[key])

disaster_key_dict.pop('NaN', None)

with open('disaster_key_dict.json', 'w') as fp:
	json.dump(disaster_key_dict, fp)

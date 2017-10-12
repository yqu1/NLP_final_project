import os
import json
import pandas as pd
import numpy as np


train = []
test = []

for fd in os.listdir('data/CrisisLexT26'):
	if fd == 'README.md':
		continue
	with open('data/CrisisLexT26/' + fd + '/' + fd + '-event_description.json') as data_file:
		ed = json.load(data_file)
		t = ed['categorization']['type']
	tf = pd.read_csv('data/CrisisLexT26/' + fd + '/' + fd + '-tweets_labeled.csv')
	msk = np.random.rand(len(tf[' Tweet Text'])) < 0.8
	print(tf[' Tweet Text'][msk])
 	for e in tf[' Tweet Text'][msk]:
 		train.append([e, t])
	for e in tf[' Tweet Text'][~msk]:
		test.append([e, t])



df_train = pd.DataFrame(train, columns = ['Tweet', 'Label'])
df_test = pd.DataFrame(test, columns = ['Tweet', 'Label'])

df_train.to_csv('train.csv')
df_test.to_csv('test.csv')


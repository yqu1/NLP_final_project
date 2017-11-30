from __future__ import division
from nltk import word_tokenize
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np
import re
import json
"""
df = pd.read_csv('disaster_data.csv')
df.dropna(axis = 0, how = 'any')
data = []
df = df.reindex(np.random.permutation(df.index))
for index, row in df.iterrows():
	if type(row['Tweet']) == float or type(row['Label']) == float:
		continue
	data.append([re.sub(r'[^a-zA-Z]', ' ', re.sub(r'@[0-9a-zA-Z]+', ' ', re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', " ", row['Tweet']))).lower(), row['Label']])
#df = df.sample(frac=1).reset_index(drop=True)
train, test = data[7000:], data[:7000]
"""
def load_data(filename):
	test = []
	with open(filename) as infile:
		test = json.load(infile)
	return test

class Naive_Bayes_Classifier:
	
	def __init__(self):
		self.c_k = {}
		self.c_k_w = {}
	
	def train(self, train):
		self.vocab = set(word for passage in train for word in word_tokenize(passage[0]))
		self.data = [[word_tokenize(i[0]), i[1]] for i in train]
		self.types = list(set([i[1] for i in train]))
		for i in self.data:
			if i[1] not in self.c_k:
				self.c_k[i[1]] = 1
			else:
				self.c_k[i[1]] += 1
		for i in self.data:
			if i[1] not in self.c_k_w:
				self.c_k_w[i[1]] = {}
			for j in i[0]:
				if j not in self.c_k_w[i[1]]:
					self.c_k_w[i[1]][j] = 1
				else:
					self.c_k_w[i[1]][j] += 1

	def test(self, test_data):
		self.vocab = self.vocab.union(set(word for passage in test_data for word in word_tokenize(passage[0])))
		test_data = [[word_tokenize(i[0]), i[1]] for i in test_data]
		for key in self.c_k_w:
			for l in self.vocab:
				if l not in self.c_k_w[key]:
					self.c_k_w[key][l] = 0
		result = []
		sum_k = {}
		for k in self.types:
			sum_k[k] = sum([self.c_k_w[k][l] for l in self.vocab])
		for i in test_data:
			prob = []
			for k in self.types:
				p_k = self.c_k[k] / sum([self.c_k[t] for t in self.types])
				p_k_w = 1
				for w in i[0]:
					temp = (self.c_k_w[k][w] + 1) / (sum_k[k] + len(self.vocab))
					p_k_w = p_k_w * temp
				prob.append(p_k * p_k_w)
			result.append(self.types[np.argmax(prob)])
		print("Accuracy: {:.2%}".format(accuracy_score(result, [i[1] for i in test_data])))
	
	def load(self):
		with open('classifier_model/model.json') as infile:
			model = json.load(infile)
			self.c_k = model["c_k"]
			self.c_k_w = model["c_k_w"]
			self.vocab = set(model["vocab"])
			self.data = model["data"]
			self.types = model["types"]
	
	def save(self):
		model = {}
		model["c_k"] = self.c_k
		model["c_k_w"] = self.c_k_w
		model["vocab"] = list(self.vocab)
		model["data"] = self.data
		model["types"] = self.types
		with open('classifier_model/model.json', 'w') as outfile:
			json.dump(model, outfile)
test = load_data('test_disaster.json')
m = Naive_Bayes_Classifier()
m.load()
m.test(test)

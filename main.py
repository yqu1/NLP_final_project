from gensim.models.keyedvectors import KeyedVectors
from DocSim import DocSim
import os


class Similarity_Model(object):
	def __init__(self):
		self.source_doc = ''
		self.target_docs = []
		self.ds = DocSim(KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin.gz', binary=True))
	
	def get_similarity(sd):
		sd = self.vectorize(sd)
		result = {}
		for fd in os.listdir('data_transform'):
			with open("data_transform/" + fd) as f:
				result[fd] = self.ds._cosine_sim(sd, self.vectorize(f.read()))
		return result
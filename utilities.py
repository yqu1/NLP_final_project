import xml.etree.ElementTree as ET
import re
import os

def clean(s):
    return re.sub('[^a-zA-Z]+', ' ', s)

def get_text_from_xml(filename):
	tree = ET.parse(filename)
	text = []
	for elem in tree.iter():
		if elem.tag == 'ORIGINAL_TEXT':
			text.append(elem.text)
	return text

def get_text_from_bio(filename, outname):
	f_out = open(outname + '.txt', 'w')
	with open(filename) as f:
		lines = f.readlines()
		temp = []
		for l in lines:
			l = l.split()
			if len(l) > 1:
				temp.append(l[0])
			else:
				f_out.write(" ".join(temp) + "\n")
				temp = []
	f_out.close()

# convert latin document to list of sentences
def docToSentences(filename):
	sentences = []
	with open(filename) as f:
		lines = f.readlines()
		for l in lines:
			l = l.strip('\n')
			if len(l) < 1 or len(l) > 512:
				continue
			sentences.append(clean(l))
		sentences = [sent.lower() for sent in sentences]
	return sentences

#create list of docs which are list of sentences, and list of labels for that doc
def createDataLabel():
	labels = []
	docs = []
	for fd in os.listdir('data_latin'):
		label = fd.split('.')[0]
		doc = docToSentences('data_latin/' + fd)
		labels.append(label)
		docs.append(doc)
	return docs, labels

#split one single training data file into multiple files
def splitFiles(filename):
	def partition(lst, n):
	    division = len(lst) / float(n)
	    return [ lst[int(round(division * i)): int(round(division * (i + 1)))] for i in xrange(n) ]

	with open(filename) as f:
		lines = f.readlines()
		for i, l in enumerate(partition(lines, 200)):
			f_out = open(filename + str(i), 'w')
			for line in l:
				f_out.write(line + "\n")
			f_out.close()

def languageList():
	lang = []
	with open("language_list.txt") as f:
		lines = f.readlines()
		for l in lines:
			if l[0] != "[":
				lang.append(l.split()[0])
	return lang



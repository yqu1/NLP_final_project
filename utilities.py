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
			sentences.append(clean(l.strip('\n')))
		sentences = [sent.lower() for sent in sentences]
	return sentences

def createDataLabel():
	labels = []
	docs = []
	for fd in os.listdir('data_latin'):
		label = fd.split('.')[0]
		doc = docToSentences('data_latin/' + fd)
		labels.append(label)
		docs.append(doc)
	return docs, labels
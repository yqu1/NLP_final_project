import xml.etree.ElementTree as ET

def get_text_from_xml(filename):
	tree = ET.parse(filename)
	text = []
	for elem in tree.iter():
		if elem.tag == 'ORIGINAL_TEXT':
			text.append(elem.text)
	return text

def get_text_from_bio(filename):
	data = list()
	with open(filename) as f:
		lines = f.readlines()
		temp = []
		for l in lines:
			l = l.split()
			if len(l) > 1:
				temp.append(l[0])
			else:
				data.append(temp)
				temp = []
	return data
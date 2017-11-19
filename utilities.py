import xml.etree.ElementTree as ET

def get_text_from_xml(filename):
	tree = ET.parse(filename)
	text = []
	for elem in tree.iter():
		if elem.tag == 'ORIGINAL_TEXT':
			text.append(elem.text)
	return text
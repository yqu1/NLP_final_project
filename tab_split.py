import csv
import os
from utilities import *
import json
import re
import string

doc_tags = {}
directory = '/afs/crc.nd.edu/user/n/nsmith9/NLP_final_project/sftype/orm/LDC2017E58_LORELEI_IL6_Incident_Language_References_for_Year_2_Eval_Unsequestered_V1.0/setE/data/annotation/situation_frame/issues'
for filename in os.listdir(directory):
    with open(directory + '/' +  filename) as tsv:
        n = 0
        for line in csv.reader(tsv, dialect="excel-tab"):
            if n == 1:
                doc_tags[line[1] + '.ltf.xml'] = line[4]
            n+=1
docroot = '/afs/crc.nd.edu/user/n/nsmith9/NLP_final_project/sftype/orm/LDC2017E58_LORELEI_IL6_Incident_Language_References_for_Year_2_Eval_Unsequestered_V1.0/setE/data/translation/il6/ltf'
text_tags = {}
regex = re.compile('[^a-zA-Z0-9 ]')
for doc in doc_tags:
    temp = get_text_from_xml(docroot + '/' + doc)
    temp = ' '.join(temp).replace('_','')
    if len(temp.strip()) > 0:
        temp = regex.sub('',temp)
        if doc_tags[doc] == 'regimechange':
            continue
        text_tags[temp] = doc_tags[doc]
text_tags = json.dumps(text_tags)
print(text_tags)

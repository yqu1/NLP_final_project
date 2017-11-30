import re
import string
import sys
import os

directory = '/afs/crc.nd.edu/user/n/nsmith9/NLP_final_project/googleTrain'
temp = ''
for filename in os.listdir(directory):
    with open(directory + '/' + filename) as f:
        temp = f.read()
        temp = re.sub('[^0-9a-zA-Z]+', ' ', temp)
    #print(temp)
    with open(directory + '/' + filename,'w') as f:        
        f.write(temp)
            
        

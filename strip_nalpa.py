import re
import string
import sys

with open(sys.argv[1]) as f:
    for each in f:
        temp = re.sub('[^0-9a-zA-Z]+', ' ', each)
        print(temp)

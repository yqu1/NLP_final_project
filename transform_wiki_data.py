from utilities import *
import os

for fd in os.listdir('data'):
	get_text_from_bio("data/" + fd, fd.replace("wikiann-", '').split(".")[0])

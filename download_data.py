from subprocess import call
from utilities import *

for l in languageList():
	call(["wget", "-P", "datatar", "https://blender04.cs.rpi.edu/~panx2/wikiann/data/" + l + ".tar.gz"])

from utilities import *
import os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-f', dest = 'filename')

args = parser.parse_args()

for fd in os.listdir(args.filename):
	splitFiles(args.filename + "/" + fd) 

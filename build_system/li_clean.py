#!/usr/bin/env python3
import os

def r(file_name):
	print(file_name)
	f = open(file_name, mode='rb')
	lines = f.read()
	f.close()
	lines=lines.decode('utf-8')
	lines=lines.split("\n")

	if lines[0]=="//":
		lines.pop(0)

	if lines[0]=="// ":
		lines.pop(0)

	n='\n'.join(lines)

#	print(n)

	f=open(file_name, mode='w')
	lines = f.write(n)
	f.close()
	#print(n)

for root, dirs, files in os.walk("./"):
	for name in files:
		full_name=os.path.join(root, name)
		if name.endswith(".c"):
			#print(full_name)
			r(full_name)

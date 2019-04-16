#!/usr/bin/python3
import os

def file_has_info(list,file_name):
	for l in list:
		if l.startswith("/** @"):
			return True

	for i in range(0,len(list)-1):
		if list[i]=="// more details." and list[i+1]=="":
			return False
	print("ohhh",file_name)
	return True

def print_info(list):
	for l in list:
		print(l)

def add_info(list,file_name,text):
	for i in range(0,len(list)-1):
		if list[i].startswith("//") and list[i].endswith("rodmack.com"):
			list[i]=="//    https://www.gpvdm.com"

		if list[i]=="// more details." and list[i+1]=="":
			i=i+2
			list.insert(i, "/** @file "+file_name)
			i=i+1
			list.insert(i, "@brief "+text)
			i=i+1
			list.insert(i, "*/")
 
def info_write(file_name,list):
	f = open(file_name,'w')
	for i in range(0,len(list)):
		f.write(list[i]+"\n")
	f.close()
	print("written.")

for root, dirs, files in os.walk("./"):
	for name in files:
		full_name=os.path.join(root, name)
		if full_name.endswith(".c") or full_name.endswith(".h"):
			f=open(full_name)
			lines = f.readlines()
			for i in range(0,len(lines)):
				lines[i]=lines[i].rstrip()
			f.close()

			if file_has_info(lines,full_name)==False:
				print_info(lines)
				print()
				print(full_name)
				a=input("Comment:")
				add_info(lines,name,a)
				info_write(full_name,lines)

			#print(lines)

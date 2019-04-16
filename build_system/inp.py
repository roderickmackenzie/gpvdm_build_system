# 
#   General-purpose Photovoltaic Device Model - a drift diffusion base/Shockley-Read-Hall
#   model for 1st, 2nd and 3rd generation solar cells.
#   Copyright (C) 2012-2017 Roderick C. I. MacKenzie r.c.i.mackenzie at googlemail.com
#
#   https://www.gpvdm.com
#   Room B86 Coates, University Park, Nottingham, NG7 2RD, UK
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License v2.0, as published by
#   the Free Software Foundation.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program; if not, write to the Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# 


## @package inp
#  Used for writing and reading .inp files from .gpvdm archives
#

#import sys
import os
import shutil
#import signal
from util_zip import replace_file_in_zip_archive
#import subprocess
from tempfile import mkstemp

#import logging
#import zipfile
from util_zip import zip_remove_file
from util_zip import write_lines_to_archive
from util_zip import read_lines_from_archive
from util_zip import archive_isfile
from util_zip import zip_lsdir


import hashlib

enable_encrypt=False

def inp_issequential_file(file_name,root):
	if file_name.startswith(root) and file_name.endswith(".inp"):
		number=file_name[len(root):-4]
		if number.isdigit()==True:
			return True
	return False

def inp_find_active_file(file_path):
	"""if you are looking for /path/to/file/cluster0.inp it will expect /path/to/file/cluster"""
	path=os.path.dirname(file_path)
	root=os.path.basename(file_path)
	files=zip_lsdir(os.path.join(path,"sim.gpvdm"))
	for f in files:
		if inp_issequential_file(f,root)==True:
			ret=str2bool(inp_get_token_value(os.path.join(path,f), "#tab_enabled"))
			if ret==True:
				return f
	return False


## List the content of an archive and directory in one list
#  @param file_name /path/to/gpvdm.sim
def inp_lsdir(file_name):
	full_path=default_to_sim_path(file_name)
	return zip_lsdir(full_path)

def inp_ls_seq_files(path,root):
	ret=[]
	files=inp_lsdir(path)

	for f in files:
		if inp_issequential_file(f,root)==True:
			ret.append(f)

	return ret

def default_to_sim_path(data):
	return data

def inp_dir_listing(file_name):
	full_path=default_to_sim_path(file_name)
	files=zip_lsdir(full_path)
	for f in files:
		print(f)

def inp_remove_file(file_name,archive="sim.gpvdm"):
	"""Remove a file from an archive"""
	full_name=default_to_sim_path(file_name)

	archive_path=os.path.join(os.path.dirname(full_name),archive)
	zip_remove_file(archive_path,os.path.basename(full_name))

def inp_read_next_item(lines,pos):
	"""Read the next item form an inp file"""
	token=lines[pos]
	pos=pos+1
	value=lines[pos]
	pos=pos+1
	return token,value,pos


def inp_replace_token_value(lines,token,replace):
	"""replace the value of a token in a list"""
	if type(lines)!=list:
		return False

	replaced=False
	for i in range(0, len(lines)):
		if lines[i]==token:
			if i+1<len(lines):
				lines[i+1]=replace
				replaced=True
				break

	return replaced

def inp_replace_token_array(lines,token,replace):
	"""replace the value of a token array in a list"""
	new_list=[]
	pos=0
	for i in range(0, len(lines)):
		new_list.append(lines[i])
		if lines[i]==token:
			pos=i+1
			new_list.extend(replace)
			break

	new_pos=0
	for i in range(pos, len(lines)):
		if len(lines[i])>0:
			if lines[i][0]=="#":
				new_pos=i
				break

	for i in range(new_pos, len(lines)):
		new_list.append(lines[i])
	
	return new_list

def inp_is_token(lines,token):
	"""Is the token in a file"""
	for i in range(0, len(lines)):
		if lines[i]==token:
			return True

	return False


def inp_add_token(lines,token,value):
	a=[]
	a.append(token)
	a.append(value)
	ret=a + lines
	return ret


def inp_update_token_array(file_path, token, replace):
	lines=[]
	base_name=os.path.basename(file_path)
	path=os.path.dirname(file_path)

	zip_file_name=os.path.join(path,"sim.gpvdm")

	lines=read_lines_from_archive(zip_file_name,os.path.basename(file_path))

	lines=inp_replace_token_array(lines,token,replace)

	write_lines_to_archive(zip_file_name,base_name,lines)

def inp_update_token_value(file_path, token, replace,archive="sim.gpvdm",id=""):
	lines=[]

	lines=inp_load_file(file_path,archive=archive)
	if lines==False:
		return False

	ret=inp_replace_token_value(lines,token,replace)
	if ret==False:
		return False

	inp_save(file_path,lines,archive=archive)

	return True


def inp_isfile(file_path,archive="sim.gpvdm"):
	file_name=default_to_sim_path(file_path)
	
	zip_file_name=os.path.join(os.path.dirname(file_name),archive)
	return archive_isfile(zip_file_name,os.path.basename(file_name))

def inp_copy_file(dest,src):
	lines=[]
	lines=inp_load_file(src)
	if lines!=False:
		inp_save(dest,lines)
		return True
	else:
		return False


def search_zip_file(file_name,archive):
	#Assume sim.gpvdm is in /a/b/c/ where mat.inp is in /a/b/c/mat.inp 
	zip_file_path=os.path.join(os.path.dirname(file_name),archive)
	if os.path.isfile(file_name)==True:
		#we found the file there so we do not care about the arhive 
		return zip_file_path

	#now try back one level
	#Using path /a/b/c/mat.inp look in /a/b/sim.gpvdm for the sim file
	if os.path.isfile(zip_file_path)==False:
		zip_file_path=os.path.join(os.path.dirname(os.path.dirname(file_name)),archive)

	return zip_file_path

def inp_load_file(file_path,archive="sim.gpvdm",mode="l"):
	"""load file"""
	if file_path==None:
		return False
	print(file_path)
	file_name=default_to_sim_path(file_path)
	#print(">",file_name)
	zip_file_path=search_zip_file(file_name,archive)#os.path.join(os.path.dirname(file_name),archive)
	#print(">>",zip_file_path)
	file_name=os.path.basename(file_name)
	ret=read_lines_from_archive(zip_file_path,file_name,mode=mode)
	return ret

def inp_save(file_path,lines,archive="sim.gpvdm"):
	"""Write save lines to a file"""

	full_path=default_to_sim_path(file_path)
	archive_path=os.path.join(os.path.dirname(full_path),archive)
	file_name=os.path.basename(full_path)
	ret= write_lines_to_archive(archive_path,file_name,lines)


	return ret

def inp_save_lines_to_file(file_path,lines):
	"""This will save lines to a text file"""
	file_name=default_to_sim_path(file_path)
	dump='\n'.join(lines)

	dump=dump.rstrip("\n")
	dump=dump.encode('utf-8')
	try:
		f=open(file_name, mode='wb')
	except:
		return False
	written = f.write(dump)
	f.close()

	return True

def inp_new_file():
	"""Make a new input file"""
	ret=[]
	ret.append("#ver")
	ret.append("1.0")
	ret.append("#end")
	return ret


def inp_get_next_token_array(lines,start):
	"""Get the next token"""
	ret=[]
	if start>=len(lines):
		return None,start

	for i in range(start,len(lines)):
		if i!=start:
			if len(lines[i])>0:
				if lines[i][0]=="#":
					break

		ret.append(lines[i])
			

	return ret,i


def inp_search_token_array(lines, token):
	"""Get an array of data assosiated with a token"""
	ret=[]
	for i in range(0, len(lines)):
		if lines[i]==token:
			pos=i+1
			for ii in range(pos,len(lines)):
				if len(lines[ii])>0:
					if lines[ii][0]=="#":
						return ret
				
				ret.append(lines[ii])
			return ret
	return False

def inp_get_token_array(file_path, token):
	"""Get an array of data assosiated with a token"""
	lines=[]
	ret=[]
	lines=inp_load_file(file_path)

	ret=inp_search_token_array(lines, token)

	return ret

def inp_get_token_value_from_list(lines, token):
	"""Get the value of a token from a list - don't use this one any more"""
	for i in range(0, len(lines)):
		if lines[i]==token:
			return lines[i+1]
	return None

def inp_search_token_value(lines, token):
	"""Get the value of a token from a list"""
	for i in range(0, len(lines)):
		if lines[i]==token:
			return lines[i+1]

	return False

def inp_get_token_value(file_path, token,archive="sim.gpvdm"):
	"""Get the value of a token from a file"""

	lines=[]
	lines=inp_load_file(file_path,archive=archive)
	if lines==False:
		return None

	ret=inp_search_token_value(lines, token)
	if ret!=False:
		return ret

	return None

def inp_sum_items(lines,token):
	my_sum=0.0
	for i in range(0, len(lines)):
		if lines[i].startswith(token)==True:
			my_sum=my_sum+float(lines[i+1])

	return my_sum


def inp_get_file_ver(archive,file_name):
	lines=[]
	lines=read_lines_from_archive(archive,file_name)

	if lines!=False:
		ver=inp_search_token_value(lines, "#ver")
	else:
		return ""

	return ver

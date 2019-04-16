#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 
# General-purpose Photovoltaic Device Model gpvdm.com - a drift diffusion
# base/Shockley-Read-Hall model for 1st, 2nd and 3rd generation solarcells.
# 
# Copyright (c) 2012-2019, Roderick C. I. MacKenzie
# All rights reserved.
# 
# 	https://www.gpvdm.com
# 	Room B86 Coates, University Park, Nottingham, NG7 2RD, UK
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the GPVDM nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL Roderick C. I. MacKenzie BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 


import os
import os.path
import argparse
import shutil
from inp import inp_get_token_value
from cal_path import subtract_paths
from util import str2bool

def safe_cpy(dest,src,f):
	if os.path.isfile(os.path.join(src,f))==True:
		shutil.copyfile(os.path.join(src,f),os.path.join(dest,f))

def cp_spectra(dest,src):
	src=os.path.join(src,"spectra")
	dest=os.path.join(dest,"spectra")
	os.makedirs(dest)

	for dirpath, dirnames, filenames in os.walk(src):
		for filename in [f for f in filenames if f=="mat.inp"]:
			mat_f_name=os.path.join(dirpath, filename)
			status=inp_get_token_value(mat_f_name, "#status")

			if status=="public_all" or status=="public":
				print("copy spectra",mat_f_name,status)
				src_mat_path=os.path.dirname(mat_f_name)

				delta_path=subtract_paths(src,src_mat_path)
				dst_mat_path=os.path.join(dest,delta_path)

				if not os.path.exists(dst_mat_path):
					os.makedirs(dst_mat_path)
				
				safe_cpy(dst_mat_path,src_mat_path,"spectra_gen.inp")
				
				safe_cpy(dst_mat_path,src_mat_path,"spectra.inp")
				
				safe_cpy(dst_mat_path,src_mat_path,"mat.inp")

				safe_cpy(dst_mat_path,src_mat_path,"spectra_eq.inp")
				

def cp_devices(dest,src):
	src=os.path.join(src,"device_lib")
	dest=os.path.join(dest,"device_lib")

	if not os.path.exists(dest):
		os.makedirs(dest)

	for dirpath, dirnames, files in os.walk(src):
		for name in files:
			if name.endswith(".gpvdm")==True:
				src_file=os.path.join(dirpath, name)
				dst_file=os.path.join(dest,subtract_paths(src,src_file))
				dst_dir=os.path.dirname(dst_file)

				private=inp_get_token_value(os.path.join(os.path.dirname(src_file),"info.inp"), "#private",archive=os.path.basename(src_file))

				if private!=None:
					if str2bool(private)==False:
						if os.path.isdir(dst_dir)==False:
							os.makedirs(dst_dir)
						shutil.copyfile(src_file,dst_file)

def cp_default_materials(dest,src):
	cp_materials(dest,src,sub_dir="blends")
	cp_materials(dest,src,sub_dir="generic")
	cp_materials(dest,src,sub_dir="helmut")
	cp_materials(dest,src,sub_dir="metal")
	cp_materials(dest,src,sub_dir="oxides")
	cp_materials(dest,src,sub_dir="polymers")
	cp_materials(dest,src,sub_dir="small_molecules")
	cp_materials(dest,src,sub_dir="gasses")
	cp_materials(dest,src,sub_dir="inorganic")
	cp_materials(dest,src,sub_dir="perovskites")	

def cp_non_default_materials(dest,src):
	cp_materials(dest,src,sub_dir="pvlighthouse.com.au")
	cp_materials(dest,src,sub_dir="refractiveindex.info")

def cp_materials(dest,src,sub_dir=None):
	
	if sub_dir==None:
		dest=os.path.join(dest,"materials")
		src=os.path.join(src,"materials")
	else:
		dest=os.path.join(dest,"materials",sub_dir)
		src=os.path.join(src,"materials",sub_dir)

	os.makedirs(dest)
	print(dest,src)
	for dirpath, dirnames, filenames in os.walk(src):
		for filename in [f for f in filenames if f=="mat.inp"]:
			mat_f_name=os.path.join(dirpath, filename)
			status=inp_get_token_value(mat_f_name, "#status")

			if status=="public_all" or status=="public":
				print("copy materials",mat_f_name,status,sub_dir)
				src_mat_path=os.path.dirname(mat_f_name)

				delta_path=subtract_paths(src,src_mat_path)
				dst_mat_path=os.path.join(dest,delta_path)
				if not os.path.exists(dst_mat_path):
					os.makedirs(dst_mat_path)
				
				safe_cpy(dst_mat_path,src_mat_path,"alpha_gen.omat")
				
				safe_cpy(dst_mat_path,src_mat_path,"n_gen.omat")
				
				safe_cpy(dst_mat_path,src_mat_path,"n_eq.inp")
				
				safe_cpy(dst_mat_path,src_mat_path,"alpha_eq.inp")
				
				safe_cpy(dst_mat_path,src_mat_path,"dos.inp")

				safe_cpy(dst_mat_path,src_mat_path,"pl.inp")

				safe_cpy(dst_mat_path,src_mat_path,"mat.inp")
				safe_cpy(dst_mat_path,src_mat_path,"fit.inp")

				safe_cpy(dst_mat_path,src_mat_path,"cost.xlsx")


				safe_cpy(dst_mat_path,src_mat_path,"alpha.omat")
				safe_cpy(dst_mat_path,src_mat_path,"n.omat")
				safe_cpy(dst_mat_path,src_mat_path,"alpha.ref")
				safe_cpy(dst_mat_path,src_mat_path,"n.ref")


				files=os.listdir(src_mat_path)
				for i in range(0,len(files)):
					if files[i].endswith(".ref")==True:
						safe_cpy(dst_mat_path,src_mat_path,files[i])

#! /usr/bin/env python3
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
import zipfile
import glob
import shutil

from build_paths import get_rpm_build_dir



def get_ver():
	zf = zipfile.ZipFile("base.gpvdm", 'r')
	read_lines = zf.read("ver.inp")
	zf.close()
	lines=read_lines.decode('utf-8')
	lines=lines.split("\n")
	ver=lines[1]
	return ver

def copy_spec():
	ver=get_ver()
	f = open("./scripts/gpvdm.spec", mode='r')
	lines = f.read()
	f.close()

	lines=lines.replace("${ver}",ver)

	f=open("./rpm/SPECS/gpvdm.spec", mode='w')
	lines = f.write(lines)
	f.close()

def make_rmp_dir(d):

	data_out=""
	if d!=None:
		data_out="&>out.dat &"

	if os.path.isdir(get_rpm_build_dir()):
		shutil.rmtree(get_rpm_build_dir())

	os.mkdir(get_rpm_build_dir())

	os.mkdir(os.path.join(get_rpm_build_dir(),"BUILD"))
	os.mkdir(os.path.join(get_rpm_build_dir(),"RPMS"))
	os.mkdir(os.path.join(get_rpm_build_dir(),"SOURCES"))
	os.mkdir(os.path.join(get_rpm_build_dir(),"SPECS"))
	os.mkdir(os.path.join(get_rpm_build_dir(),"SRPMS"))
	os.mkdir(os.path.join(get_rpm_build_dir(),"BUILDROOT"))

	if os.path.isdir('./pub/build')==False:
		d.msgbox("You have not publishe the code")
		return
	for file in glob.glob("./pub/build/*.tar"):
		shutil.copy(file, "./rpm/SOURCES/")

	copy_spec()

	os.system("rpmbuild -v --target x86_64 -ba --define \"_topdir "+os.getcwd()+"/rpm/"+"\" --noclean ./rpm/SPECS/gpvdm.spec "+data_out)
	if d!=None:
		ret=d.tailbox("out.dat", height=None, width=100)

	for file in glob.glob("./rpm/RPMS/x86_64/*.rpm"):
		shutil.copy(file, "./pub/")

	if os.path.isdir(get_rpm_build_dir()):
		shutil.rmtree(get_rpm_build_dir())



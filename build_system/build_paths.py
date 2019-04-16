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
import platform

from inp import inp_get_token_value

package_path=None
pub_path=None
rpm_build_dir=None

def get_ver():
	return inp_get_token_value("ver.inp", "#core")

def build_setup_paths():
	global package_path
	global pub_path
	global rpm_build_dir

	ret=platform.dist()
	distro_name=ret[0]
	os_numer=ret[1]
	os_cute_name=ret[2].replace(" ","_")

	distro=ret[0]+"_"+ret[1]
	package_path=os.path.join(os.getcwd(),"package_lib",distro_name,os_numer+"_"+os_cute_name)
	if os.path.isdir(package_path)==False:
		os.makedirs(package_path)

	pub_path=os.path.join(os.getcwd(),"pub")
	rpm_build_dir=os.path.join(os.getcwd(),"rpm")

def get_package_path():
	global package_path
	return package_path

def get_pub_path():
	global pub_path
	return pub_path

def get_rpm_build_dir():
	global rpm_build_dir
	return rpm_build_dir

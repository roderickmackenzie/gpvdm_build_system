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
try:
	from dialog import Dialog
except:
	from menu import Dialog

from to_web import to_github
from to_web import src_to_web
from publish import publish_src
from publish import publish_materials_to_web

def publish_menu(d):
	code, tag = d.menu("publish for:",
		               choices=[("(windows)", "Publish for windows"),
								("(github)", "Publish to github"),
								("(materials)", "Publish to the materials"),
								])
	if code == d.OK:
		if tag=="(windows)":
			publish_src(d,publication_mode="windows")
			os.system("echo \"done\" >log.txt ")
			ret=d.tailbox("log.txt", height=None, width=100)

#		if tag=="(debian)":
#			os.system("./pub.sh --debian")

		#if tag=="(linux)":
		#	publish_src(d,publication_mode="gpl_distro")

		if tag=="(github)":
			publish_src(d,publication_mode="github")
			os.system("echo \"done\" >log.txt ")
			ret=d.tailbox("log.txt", height=None, width=100)
			to_github(d)
			src_to_web(d)

		if tag=="(materials)":
			publish_materials_to_web(d)

		print(tag)

#!/usr/bin/env python3
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
import sys
from build_log import log

apt_present=True
try:
	import apt
except:
	apt_present=False

if apt_present==True:
	class LogInstallProgress(apt.progress.base.InstallProgress):
		def conffile(self, current, new):
			log("conffile prompt: "+ current+" " +new)

		def processing(self, pkg, stage):
			log("Processing " + pkg+ " stage: "+ stage)

		def error(self, pkg, errormsg):
			log("Package "+ pkg+ " error: "+ errormsg)

		def finish_update(self):
			log("Installation is complete")

		def status_change(self, pkg, percent, status):
			log("Package: "+ pkg + " at "+ str(percent) + " -> "+ status)

		def dpkg_status_change(self, pkg, status):
			log("Package "+ pkg + ", Status: "+ status)
	
		def start_update(self):
			log("start")

		def finish_update(self):
			log("Closing package cache")

def apt_install(d,my_list):
	f=open("out.dat", "w+")
	f.close()

	global apt_present
	if apt_present==False:
		d.msgbox("apt-get is not present on system are you sure you are on a Debian/Ubunu system?")
		return False

	newpid = os.fork()
	if newpid == 0:
		#dev_null = open('/dev/null', 'w')
		#os.dup2(dev_null, sys.stdout.fileno())                         
                                   
		#os.dup2(dev_null, sys.stderr.fileno())  
		cache = apt.cache.Cache()
		log("update")
		cache.update()
	




		log("Installing "+str(len(my_list))+" packages")
		installed=0
		already_installed=0
		for i in range(0,len(my_list)):
			if my_list[i] in cache:
				pkg = cache[my_list[i]]
				if pkg.is_installed:
					text=my_list[i]+" (Installed)"
					already_installed=already_installed+1
				else:
					text=my_list[i]+" (Will install)"
					installed=installed+1
					pkg.mark_install()

				log(text)
			else:
				log(my_list[i]+" Not found")
		#try:
		log("commit (this could take a while.)")
		prog=LogInstallProgress()
		cache.commit(install_progress=prog)
		log("\nInstalled= "+str(installed)+" Already installed "+str(already_installed))
		#except:
		#	log( "Sorry, package installation failed")

		cache.close()
		sys.exit()

#apt_install(["python3-xstatic-bootswatch"])
#pause = input('wait')

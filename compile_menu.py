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

from make_m4 import make_m4

from pathlib import Path
from shutil import copyfile

def test(d):
	if d.yesno("Run gpvdm") == d.OK:
		os.system("./go.o  >log.txt 2>log.txt &")
		et=d.tailbox("log.txt", height=None, width=150)

def make_all(d):
	if d.yesno("Run make clean") == d.OK:
		os.system("cd gpvdm_core;make clean >../log.txt 2>../log.txt ;cd ../gpvdm_gui; make clean >../log.txt 2>../log.txt ;cd ../gpvdm_data; make clean >../log.txt 2>../log.txt&")
		et=d.tailbox("log.txt", height=None, width=150)

	if d.yesno("Run make in gpvdm_core") == d.OK:
		jobs=os.cpu_count()
		os.system("cd gpvdm_core; make  -j "+str(jobs)+" >../log.txt 2>../log.txt &")
		et=d.tailbox("log.txt", height=None, width=150)

	if d.yesno("Run make in gpvdm_gui") == d.OK:
		jobs=os.cpu_count()
		os.system("cd gpvdm_gui; make  -j "+str(jobs)+" >../log.txt 2>../log.txt &")
		et=d.tailbox("log.txt", height=None, width=150)

	if d.yesno("Run make in gpvdm_data") == d.OK:
		jobs=os.cpu_count()
		os.system("cd gpvdm_data; make  -j "+str(jobs)+" >../log.txt 2>../log.txt &")
		et=d.tailbox("log.txt", height=None, width=150)

    	#d.msgbox("You have been warned...")

def build_configure(directory):
	my_dir=os.getcwd()
	os.chdir(os.path.join(my_dir,directory))
	os.system("aclocal")
	os.system("automake --add-missing")
	os.system("automake")
	os.system("autoconf")
	os.chdir(my_dir)

def build_configure_all():
	build_configure("gpvdm_core")
	build_configure("gpvdm_gui")
	build_configure("gpvdm_data")

def configure_for_fedora(d):
	make_m4(hpc=False, win=False,usear=True)
	#d.infobox("aclocal", width=0, height=0, title="configure")
	build_configure_all()
	os.system("cd gpvdm_core;./configure CPPFLAGS=\"-I/usr/include/suitesparse/\" --datadir=\"/usr/share/\" --bindir=\"/usr/bin/\" &>../log.txt  &")
	et=d.tailbox("log.txt", height=None, width=100)

	os.system("cd gpvdm_gui;./configure &>../log.txt  &")
	et=d.tailbox("log.txt", height=None, width=100)

	os.system("cd gpvdm_data;./configure &>../log.txt  &")
	et=d.tailbox("log.txt", height=None, width=100)

def configure_for_debian(d):
	make_m4(hpc=False, win=False,usear=True)
	#d.infobox("aclocal", width=0, height=0, title="configure")
	build_configure_all()
	os.system("cd gpvdm_core;./configure CPPFLAGS=\"-I/usr/include/\" --datadir=\"/usr/share/\" --bindir=\"/usr/bin/\" >../log.txt 2>../log.txt &")
	et=d.tailbox("log.txt", height=None, width=100)

	os.system("cd gpvdm_gui;./configure &>../log.txt  &")
	et=d.tailbox("log.txt", height=None, width=100)

	os.system("cd gpvdm_data;./configure &>../log.txt  &")
	et=d.tailbox("log.txt", height=None, width=100)


def configure_for_ubuntu(d):
	make_m4(hpc=False, win=False,usear=True)

	build_configure_all()

	os.system("cd gpvdm_core;./configure CPPFLAGS=\"-I/usr/include/\" --datadir=\"/usr/share/\" --bindir=\"/usr/bin/\" >../log.txt 2>../log.txt &")
	et=d.tailbox("log.txt", height=None, width=100)

	os.system("cd gpvdm_gui;./configure &>../log.txt  &")
	et=d.tailbox("log.txt", height=None, width=100)

	os.system("cd gpvdm_data;./configure &>../log.txt  &")
	et=d.tailbox("log.txt", height=None, width=100)

def configure_for_ubuntu_with_flat_install(d):
	make_m4(hpc=False, win=False,usear=True)

	build_configure_all()

	os.system("cd gpvdm_core;./configure CPPFLAGS=\"-I/usr/include/\"  --enable-noplots --enable-noman --docdir=/ --datadir=/ --bindir=/  --libdir=/   >../log.txt 2>../log.txt &")
	et=d.tailbox("log.txt", height=None, width=100)

	os.system("cd gpvdm_gui;./configure  --enable-nodesktop --enable-noman --docdir=/ --datadir=/ --bindir=/  --libdir=/  &>../log.txt  &")
	et=d.tailbox("log.txt", height=None, width=100)

	os.system("cd gpvdm_data;./configure  --docdir=/ --datadir=/ --bindir=/  --libdir=/ &>../log.txt  &")
	et=d.tailbox("log.txt", height=None, width=100)

def configure_for_centos_hpc(d):
	make_m4(hpc=True, win=False,usear=False)

	build_configure_all()

	os.system("cd gpvdm_core;./configure CPPFLAGS=\"-I/usr/include/\" --enable-hpc --enable-noimages --enable-noplots --enable-noman --enable-nodesktop --enable-nodevicelib --enable-nohtml >../log.txt 2>../log.txt &")

	et=d.tailbox("log.txt", height=None, width=100)

	os.system("cd gpvdm_gui;./configure &>../log.txt  &")
	et=d.tailbox("log.txt", height=None, width=100)

def configure_for_centos(d):
	make_m4(hpc=False, win=False,usear=True)

	build_configure_all()

	os.system("cd gpvdm_core;./configure CPPFLAGS=\"-I/usr/include/\" >../log.txt 2>../log.txt &")
	et=d.tailbox("log.txt", height=None, width=100)

	os.system("cd gpvdm_gui;./configure &>../log.txt  &")
	et=d.tailbox("log.txt", height=None, width=100)

	os.system("cd gpvdm_data;./configure &>../log.txt  &")
	et=d.tailbox("log.txt", height=None, width=100)

	make_all(d)

def configure_for_arch(d):
	make_m4(hpc=False, win=False,usear=True)

	build_configure_all()

	os.system("cd gpvdm_core;./configure CPPFLAGS=\"-I/usr/include/\" >../log.txt 2>../log.txt &")
	et=d.tailbox("log.txt", height=None, width=100)

	os.system("cd gpvdm_gui;./configure &>../log.txt  &")
	et=d.tailbox("log.txt", height=None, width=100)

	os.system("cd gpvdm_data;./configure &>../log.txt  &")
	et=d.tailbox("log.txt", height=None, width=100)

	make_all(d)

def configure_for_windows(d):
	make_m4(hpc=False, win=True,usear=True)

	build_configure_all()

	home=str(Path.home())
	flags="-I"+home+"/windll/libzip/libzip-0.11.2/lib/ -I"+home+"/windll/SuiteSparse-3.0.0/SuiteSparse/UFconfig/ -I"+home+"/windll/SuiteSparse-3.0.0/SuiteSparse/AMD/Include/ -I"+home+"/windll/SuiteSparse-3.0.0/SuiteSparse/UMFPACK/Include/"
	#+home+"-I/windll/OpenCL-Headers-master/"
	#+"-I/windll/gsl-1.16/
	os.system("cd gpvdm_core; ./configure --host=i686-w64-mingw32 CPPFLAGS=\""+flags+"\"  --enable-noplots --enable-noman --docdir=/ --datadir=/ --bindir=/  --libdir=/  >../log.txt 2>../log.txt &")
	ret=d.tailbox("log.txt", height=None, width=100)

	os.system("cd gpvdm_gui;./configure --enable-nodesktop --enable-noman --docdir=/ --datadir=/ --bindir=/  --libdir=/ &>../log.txt  &")
	et=d.tailbox("log.txt", height=None, width=100)

	os.system("cd gpvdm_data;./configure --docdir=/ --datadir=/ --bindir=/  --libdir=/ &>../log.txt  &")
	et=d.tailbox("log.txt", height=None, width=100)

def configure_autodetect(d):
	import platform
	plat=platform.dist()[0].lower()
	chipset=os.uname().machine
	configured=False
	if d.yesno("Configure for "+plat+" "+chipset) == d.CANCEL:
		return
	if plat=="fedora":
		configured=True
		configure_for_fedora(d)
	elif plat=="debian":
		configured=True
		configure_for_debian(d)
	elif plat=="ubuntu":
		configured=True
		configure_for_ubuntu(d)
	elif plat=="centos":
		configured=True
		configure_for_centos_hpc(d)
	elif plat=="arch":
		configured=True
		configure_for_arch(d)

	if configured==True:
		make_all(d)
		d.msgbox("Built")
	else:
		d.msgbox("Can't auto configure for this platform.")

def select_distro_menu(d):
	if os.geteuid() == 0:
		d.msgbox("Don't do a build as root")
		return
	code, tag = d.menu("build for:",
		               choices=[("(back)", "back"),
								("(fedora)", "fedora (x86_64)"),
								("(debian)", "debian (x86_64)"),
								("(raspberry)", "Raspberry (ARM)"),
								("(centos)", "CENTOS (x86_64)"),
								("(mint)", "Mint (x86_64)"),
								("(ubuntu)", "Ubuntu (x86_64)"),
								("(ubuntu_flat)", "Ubuntu flat install dir (x86_64)"),
								("(suse)", "Open Suse (x86_64)"),
								("(arch)", "Arch (x86_64)"),
								("(debian-i386)","Debian (i386)"),
								("(default)", "generic Linux (x86_64)")
								])

	if code == d.OK:
		if tag=="(back)":
			configure_menu(d)

		if tag=="(default)":
			make_m4(hpc=False, win=False,usear=True)
			#d.infobox("aclocal", width=0, height=0, title="configure")
			build_configure_all()
			os.system("./configure CPPFLAGS=\"-I/usr/include/\"  &>../log.txt &")
			et=d.tailbox("log.txt", height=None, width=100)

			make_all(d)

			d.msgbox("Built")

		if tag=="(fedora)":
			configure_for_fedora(d)
			make_all(d)
			d.msgbox("Built")


		if tag=="(debian)":
			configure_for_debian(d)
			make_all(d)
			d.msgbox("Built")

		if tag=="(raspberry)":
			make_m4(hpc=False, win=False,usear=True)

			os.system("aclocal")
			os.system("autoconf")
			os.system("autoheader")
			os.system("automake")
			os.system("automake --add-missing")
			os.system("automake")
			os.system("cd gpvdm_core; ./configure CPPFLAGS=\"-I/usr/include/\" --host=arm-linux >../log.txt 2>../log.txt &")
			et=d.tailbox("log.txt", height=None, width=100)

			make_all(d)

			d.msgbox("Built")


		if tag=="(centos)":
			configure_for_centos(d)

			d.msgbox("Built")


		if tag=="(mint)":
			make_m4(hpc=False, win=False,usear=True)

			build_configure_all()

			os.system("cd gpvdm_core; ./configure CPPFLAGS=\"-I/usr/include/\" >../log.txt 2>../log.txt &")
			et=d.tailbox("log.txt", height=None, width=100)

			make_all(d)

			d.msgbox("Built")

		if tag=="(ubuntu)":
			configure_for_ubuntu(d)
			make_all(d)
			d.msgbox("Built")

		if tag=="(ubuntu_flat)":
			configure_for_ubuntu_with_flat_install(d)
			make_all(d)
			d.msgbox("Built")

		if tag=="(suse)":
			make_m4(hpc=False, win=False,usear=True)

			build_configure_all()

			os.system("cd gpvdm_core; ./configure CPPFLAGS=\"-I/usr/include/\" >../log.txt 2>../log.txt &")
			et=d.tailbox("log.txt", height=None, width=100)

			make_all(d)

			d.msgbox("Built")

		if tag=="(arch)":
			configure_for_arch(d)

			d.msgbox("Built")

		if tag=="(debian-i386)":

			make_m4(hpc=False, win=False,usear=True)
			#d.infobox("aclocal", width=0, height=0, title="configure")
			build_configure_all()
			os.system("cd gpvdm_core;./configure CPPFLAGS=\"-I/usr/include/\" --host=i686-linux-gnu --build=i686-linux-gnu CC=\"gcc -m32\" CXX=\"g++ -m32\" >../log.txt 2>../log.txt &")
			et=d.tailbox("log.txt", height=None, width=100)

			make_all(d)

			d.msgbox("Built")


		
def compile_menu(d):
	if os.geteuid() == 0:
		d.msgbox("Don't do a build as root")
		return
	code, tag = d.menu("build for:",
		               choices=[("(auto)", "Configure for distro/architecture"),
								("(select)", "Select distro by hand"),
								("(docs)", "Build code documentation")
								])

	if code == d.OK:
		if tag=="(auto)":
			configure_autodetect(d)

		if tag=="(select)":
			select_distro_menu(d)

		if tag=="(docs)":
			if os.path.isdir("./code_docs")==False:
				os.mkdir("code_docs")

			os.system("doxygen ./docs/doxygen_gui.config >../log.txt 2>../log.txt &")
			os.system("doxygen ./docs/doxygen_core.config >../log.txt 2>../log.txt &")
			ret=d.tailbox("log.txt", height=None, width=100)
			#publish_code_docs()
			d.msgbox("Done")





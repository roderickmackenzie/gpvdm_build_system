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
try:
	from dialog import Dialog
except:
	from menu import Dialog

apt=True
dnf=True
from apt_install import apt_install
from dnf_install import dnf_install

from generic_install import generic_install
import platform


def install_suse(d):
	#to compile C
	tools=["gcc","autoconf","make","libtool","automake","libzip","libzip-devel","suitesparse-devel","help2man","gsl-devel","gettext-tools","dbus-1-devel","zlib-devel","gnuplot"]

	#for gui
	python=["python-qt5-utils","python3-qt5-devel","python3-qt5","python3-pycrypto","python3-numpy","python3-matplotlib","python3-matplotlib-qt-shared","python3-psutil","python3-openpyxl","python3-opengl","texlive"]

	#building rpm
	devel=["rpmbuild","unifdef"]

	all=[]
	all.extend(tools)
	all.extend(python)
	all.extend(devel)

	dnf_install(d,all)




def install_raspbian(d):

	libs=["libsuitesparse-dev","indent","unifdef","libsuitesparse-dev","libssl-dev","libedbus-dev","libzip-dev","libgsl0-dev","libmatheval-dev","help2man","pluma","build-essential","imagemagick","license-reconcile","autoconf","librsvg2-bin"]

	#python
	python=["python3-numpy","python3","python3-matplotlib","python3-pyqt5.qtopengl","python3-opengl","python3-numpy","python3-crypto","python3-dbus.mainloop.pyqt5","python3-psutil"]

	#usefull tools
	tools=["rsync","pluma","build-essential","imagemagick","license-reconcile","autoconf","python-bashate","codespell","apt-file","gettext-lint","inkscape","pep8","i18nspector","qttools5-dev-tools","qtcreator"]

	all=[]
	all.extend(libs)
	all.extend(python)
	all.extend(tools)

	apt_install(d,all)


def install_centos(d):
	libs=["suitesparse-devel", "openssl-libs", "openssl-libs-devel", "openssl-devel", "libzip", "libzip-devel", "gsl-devel", "blas-devel", "mencoder",  "unifdef", "indent","zlib-devel" ,"libzip-devel", "suitesparse-devel", "openssl-devel", "gsl-devel" ,"libcurl-devel" ,"blas-devel" ,"help2man" ,"librsvg2-tools", "libmatheval-devel" ,"valgrind", "@development-tools" ,"fedora-packager", "pciutils-devel" ,"mingw32-gcc"]
	libs=" ".join(libs)

	tools=["unifdef", "indent", "ghostscript","ImageMagick"]
	tools=" ".join(tools)+" "

	python=["python34", "python34-matplotlib",  "python34-inotify", "python34-crypto", "python34-awake" ,"numpy" ,"notify34-python", "python34-inotify.noarch" ]
	python=" ".join(python)+" "

	devel=["epel-release"]
	devel=" ".join(python)+" "

	os.system("sudo yum install "+ libs+tools+python+devel+" &>out.dat &")



def install_mint(d):
	python=["python3","python3-matplotlib","python3-pyqt5.qtopengl","python3-opengl","python3-numpy","python3-crypto","python3-dbus.mainloop.pyqt5"]

	libs=["libsuitesparse-dev","indent","unifdef","libsuitesparse-dev","libssl-dev","libedbus-dev","libzip-dev","libgsl0-dev","libmatheval-dev","help2man","pluma","build-essential","imagemagick","license-reconcile","autoconf","codespell","librsvg2-bin"]

	tools=["rsync","pluma","build-essential","convert","imagemagick","license-reconcile","autoconf","python-bashate","codespell","complexity","apt-file","pofileSpell","gettext-lint","inkscape","spellintian","pep8","i18nspector","python-bashate","automake"]

	devel=["dh-virtualenv","debhelper"]

	all=[]

	all.extend(python)
	all.extend(libs)
	all.extend(tools)
	all.extend(devel)

	apt_install(d,all)





def package_menu(d):
	if os.geteuid() != 0:
		d.msgbox("You need to be root to install packages")
		return
	menu=[]
	plat=platform.dist()[0].lower()
	chipset=os.uname().machine
	configured=False

	if d.yesno("Install packages needed by gpvdm to run on the platform: "+plat+" "+chipset) == d.CANCEL:
		return
	if plat=="fedora":
		configured=True
		generic_install(d,"scripts/packages_fedora.sh")
	elif plat=="debian":
		configured=True
		generic_install(d,"scripts/packages_debian.sh")
	elif plat=="ubuntu":
		configured=True
		generic_install(d,"scripts/packages_ubuntu.sh")
	elif plat=="centos":
		configured=True
		install_centos(d)
		ret=d.tailbox("out.dat", height=None, width=100)
	elif plat=="arch":
		configured=True
		generic_install(d,"scripts/packages_arch.sh")
	elif plat=="mint":
		configured=True
		install_mint(d)
		ret=d.tailbox("out.dat", hieght=None, width=100)
	elif plat=="suse":
		configured=True
		install_suse(d)
		ret=d.tailbox("out.dat",height=None, width=100)
	elif plat=="raspbian":
		configured=True
		install_raspbian(d)
		ret=d.tailbox("out.dat",height=None, width=100)
	else:
		d.msgbox("I don't know how to install packages for your distribution, file a bug report if you would like your distro added to gpvdm.")


if __name__ == "__main__":
	d = Dialog(dialog="dialog")

	d.set_background_title("gpvdm build configure")
	package_menu(d)

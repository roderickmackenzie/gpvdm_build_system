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
	import pyinotify
except:
	print("python3-pyinotify is not installed")
	sys.exit(0)

import re
import time

class ModHandler(pyinotify.ProcessEvent):
	def __init__(self,file_name):
		self.fname=file_name
		self.p=0
		try:
			self.f=open(self.fname,"r", encoding="latin-1")
			sys.stdout.write(self.f.read())
			sys.stdout.flush()
			self.p = self.f.tell()
			self.f.close()
		except:
			pass

	def process_IN_MODIFY(self, evt):
		try:
			self.f=open(self.fname,"r", encoding="latin-1")
			self.f.seek(0,2)
			size = self.f.tell()
			if self.p>size:
				self.p=0
			self.f.seek(self.p)
			r=self.f.read()
			pos=r.rfind('\n')
			if pos!=-1:
				r=r[:pos]
				self.f.seek(self.p+len(r))
				r=re.sub(r'[^\x00-\x7F]+',' ', r)
				print(r, end='', flush=True)
				#sys.stdout.write(">"+r+"<")
				#sys.stdout.flush()
				self.p = self.f.tell()
			self.f.close()
		except:
			pass

def tail(fname):
	handler = ModHandler(fname)
	wm = pyinotify.WatchManager()
	notifier = pyinotify.ThreadedNotifier(wm, handler)
	notifier.daemon=True
	wdd = wm.add_watch(fname, pyinotify.ALL_EVENTS)

	notifier.start()

	while(1):
		time.sleep(1.0) 
		if os.path.isfile(fname)==True:
			if (time.time() - os.stat(fname).st_mtime)>2:
				break
		else:
			break

#	input("Press Enter to continue...")
	print("")
	notifier.stop()


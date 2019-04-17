gpvdm - Simulate Organic Solar Cells, Inorganic solar cells, OLEDs and OFETs
============================================================================

Gpvdm is a tool to simulate thin film optoelectronic devices including, organic solar cells, perovskite solar cells, thin film light emitting diodes and transistors.  The model contains 1/2D electrical and an optical 
solvers, enabling both current/voltage characteristics to be simulated as well 
as the optical properties of a device. The model and it's easy to use 
graphical interface is available for both Linux and Windows, x86 and ARM.
The model can simulate:

- Steady state measurements such as JV curves, and Suns-Voc
- Transient measurements such as CELIV, Transient photo current measurements and Transient photocurrent measurements.
- Full optical model taking into account reflection at interfaces and absorption.
- Calculation of reflection profile
- OLEDs
- 2D OFETS
- Fitting to experimental data

The physical model solves both electron and hole drift-diffusion, and carrier 
continuity equations in position space to describe the movement of charge 
within the device. The model also solves Poisson's equation to calculate the 
internal electrostatic potential. Recombination and carrier trapping are 
described within the model using a Shockley-Read-Hall (SRH) formalism, the 
distribution of trap sates can be arbitrarily defined. A fuller description of 
the model can be found in the at https://www.gpvdm.com, in the associated
publications  and in the manual.

The model makes it easy to study the influence of material parameters such as 
mobility, energetic disorder, doping and recombination cross-sections on device 
performance. All internal device parameters such as current density, charge 
density, distribution of trapped carriers in position and energy space are 
accessible either through the graphical interface or directly through output 
files. 

Installing/building gpvdm
==============

1 Windows
----------

I would recommend downloading the binary from the gpvdm web page.  Double click on the installer and follow the instructions.  I always keep the windows exe up-to date and on the latest stable release.

2 Linux
--------
For Linux I **recommend** you compile from source code.  I do provide some rpm/deb packages on the web page, but I don't update them very often, if you really want an updated RPM/DEB package let me know.

2.1 Linux from source the easy way
----------------------------------
Download the gpvdm build system by issuing the command 

~~~~
git clone  https://github.com/roderickmackenzie/gpvdm_build_system
~~~~

Make sure you have python3-dialog installed on your system, if you don't issue the command:
~~~~
apt-get install python3-dialog
~~~~
on an Ubuntu/Debian system or 
~~~~
yum install python3-dialog
~~~~
on a redhat/fedora/centos system.  To start the build process, issue the commands

~~~~
cd gpvdm_build_system
sudo ./build
~~~~

Firstly select (packages) and let the installer install the dependencies needed to compile gpvdm.  Once finished exit the installer and re-run ./gpvdm as a normal user.  It will prompt you to download the source code to gpvdm, just say yes to all questions.  Once the source code has downloaded, you will again be presented with a blue screen, select compile and answer yes to all questions.  You should be left with a file called gpvdm, in the root build directory to run it type:

~~~~
./gpvdm
~~~~

2.2 Linux from source the hard way
----------------------------------
Gpvdm consists of four independent components:
1. gpvdm_core: This is the core solver of gpvdm, which does all the complex math, written in C.
2. gpvdm_gui: This is the GUI to gpvdm, you don't need it to run the model, but it makes it much easier. It is written in python.
3. gpvdm_data: This is a database of materials, light sources and documentation.
4. gpvdm_build_system: This is used to build all the code.

Download the the build system
~~~~
git clone  https://github.com/roderickmackenzie/gpvdm_build_system
cd gpvdm_build_system
~~~~
enter the build directory
~~~~
cd gpvdm_build_system
~~~~
Get the rest of the source code
~~~~
git clone  https://github.com/roderickmackenzie/gpvdm_core
git clone  https://github.com/roderickmackenzie/gpvdm_gui
git clone  https://github.com/roderickmackenzie/gpvdm_data
~~~~

You are now going to install the packages need by gpvdm to run, go to the directory:
~~~~
cd build_system/dependency_scripts
~~~~

And find, the script relating to your distribution, and run it.  It will install all the packages needed by gpvdm to run.

Issue the following commands in gpvdm_core, gpvdm_data, and gpvdm_gui in turn

~~~~
aclocal
automake --add-missing
automake
autoconf
./configure CPPFLAGS="-I/usr/include/suitesparse/"
make
~~~~

You may have to replace /usr/include/suitesparse/ with a different path depending on your distro.  I know these instructions sound complex, which is the reason I suggest you use my build tool.....  Any issues get back to me and I will fix them.

Help using gpvdm
----------------
I'm very happy to provide help in using gpvdm, or if you wold prefer I am 
equally happy to collaborate and model your data for you. See the contact page.


More information
----------------
More information can be found on the home page https://www.gpvdm.com

Licensing
---------
gpvdm comes in three parts with different licenses:
- gpvdm_core: This is licensed under a 3-clause BSD license.
- gpvdm_gui: This is licensed under a GPLv2 license.
- gpvdm_build_system: This is also licensed under a BSD 3-clause license
- gpvdm_data: Creative Commons BY-CC.
See the individual license files for details.
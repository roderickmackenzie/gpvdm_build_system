gpvdm - Simulate Organic Solar Cells, Inorganic solar cells, OLEDs and OFETs
============================================================================

Gpvdm is an organic solar cells model. It is specifically designed to 
simulate bulk-heterojuncton organic solar cells, such as those based on the 
P3HT:PCBM material system. The model contains both an electrical and an optical 
solver, enabling both current/voltage characteristics to be simulated as well 
as the optical modal profile within the device. The model and it's easy to use 
graphical interface is available for both Linux and Windows.
The model can simulate:

    -Dark JV curves
    -Light JV curves
    -Dark CELIV transients
    -Light CELIV transients
    -Voltage transients of an arbitrary shape
    -Full optical model taking into account reflection at interfaces and absorption.
    -Calculation of reflection profile
    -Ability to simulate OLEDs

The physical model solves both electron and hole drift-diffusion, and carrier 
continuity equations in position space to describe the movement of charge 
within the device. The model also solves Poisson's equation to calculate the 
internal electrostatic potential. Recombination and carrier trapping are 
described within the model using a Shockley-Read-Hall (SRH) formalism, the 
distribution of trap sates can be arbitrarily defined. A fuller description of 
the model can be found in the at https://www.gpvdm.com, in the associated
publications  and in the manual.
Example simulations

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

I would recommend downloading the binary from the gpvdm web page.  Double click on the installer and follow the instructions.

2 Linux
--------
For Linux I **recommend** you compile from source code.  I do provide some rpm/deb packages on the web page, but I don't update them very often, if you really want an RPM/DEB package let me know.

2.1 Linux from source the easy way
----------------------------------
Download the gpvdm build system by issuing the command 

~~~~
git clone  https://github.com/roderickmackenzie/gpvdm_build_system
~~~~

Make sure you have python3-dialog installed on your system, if you don't issue the commands on a debian/ubuntu system:
~~~~
apt-get install python3-dialog
~~~~
or on a redhat/fedora/centos system
~~~~
yum install python3-dialog
~~~~

To start the build process, issue the commands

~~~~
cd gpvdm_build_system
sudo ./build
~~~~

Firstly select (packages) and let the installer install the packages needed to compile gpvdm.  Once finished exit the installer and re-run ./gpvdm as a normal user.  It will prompt you to download the source code to gpvdm, just say yes to all questions.  Once the source code has downloaded, you will again be presented with a blue screen, select compile and answer yes to all questions.

2.2 Linux from source the hard way
----------------------------------
Gpvdm consists of four independent components:
1. gpvdm_core: This is the core solver of gpvdm, which does all the complex math, written in C.
2. gpvdm_gui: This is the GUI to gpvdm, you don't need to run the model, but it makes it much easier. It is written in python.
3. gpvdm_data: This is a database of materials.
4. gpvdm_build_system: This is used to build all the code.

Download the components of gpvdm
~~~~
git clone  https://github.com/roderickmackenzie/gpvdm_build_system
cd gpvdm_build_system
~~~~

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

Issue the following commands in gpvdm_core, gpvdm_data, and gpvdm_gui

~~~~
aclocal
automake --add-missing
automake
autoconf
./configure CPPFLAGS="-I/usr/include/suitesparse/"
make
~~~~

You may have to replace /usr/include/suitesparse/ with a different path depending on your distro.  I know these instructions sound complex, which is the reason you use my build too.....  Any issues get back to me and I will fix them.

Help using gpvdm
----------------
I'm very happy to provide help in using gpvdm, or if you wold prefer I am 
equally happy to collaborate and model your data for you. See the contact page.


More information
----------------
More information can be found on the home page https://www.gpvdm.com

Licensing
---------
gpvdm comes in two parts, gpvdm_core and gpvdm_gui.  They are independent programs, gpvdm_core is licensed under the 3-clause BSD license, gpvdm_gui is licensed under the GPL v2.


# mg-pybooth
MG own photo booth project

# Raspberry Pi

## GPIO Header
A powerful feature of the Raspberry Pi is the row of GPIO (general-purpose input/output) pins along the top edge of the board. A 40-pin GPIO header is found on all current Raspberry Pi boards, although it is unpopulated on Raspberry Pi Zero, Raspberry Pi Zero W, and Raspberry Pi Zero 2 W. The GPIO headers on all boards have a 0.1in (2.54mm) pin pitch.

Below the schema in ASCII art:

```text
                  Pin #  
           +3V3 [01] [02] +5V
 SDA1 / GPIO  2 [03] [04] +5V
 SCL1 / GPIO  3 [05] [06] GND
        GPIO  4 [07] [08] GPIO 14 / TXD0
            GND [09] [10] GPIO 15 / RXD0
        GPIO 17 [11] [12] GPIO 18
        GPIO 27 [13] [14] GND
        GPIO 22 [15] [16] GPIO 23
           +3V3 [17] [18] GPIO 24
 MOSI / GPIO 10 [19] [20] GND
 MISO / GPIO  9 [21] [22] GPIO 25
  CLK / GPIO 11 [23] [24] GPIO  8 / CE0#
            GND [25] [26] GPIO  7 / CE1#
ID_SD / GPIO  0 [27] [28] GPIO  1 / ID_SC
        GPIO  5 [29] [30] GND
        GPIO  6 [31] [32] GPIO 12
        GPIO 13 [33] [34] GND
 MISO / GPIO 19 [35] [36] GPIO 16 / CE2#
        GPIO 26 [37] [38] GPIO 20 / MOSI
            GND [39] [40] GPIO 21 / SCLK
```

http://weyprecht.de/2015/11/30/raspberry-pi-ascii-art/

## Leds

For this project I'm using a 5050 non-addressable led strip, which you can buy for ~10 € on discount stores on e-commerce.
This is a great guide on how to configure the hardware and software to set it up:
https://lededitpro.com/rgb-led-strip-with-a-raspberry-pi/

And this is a video with step-by-step set up: https://www.youtube.com/watch?v=96uqxLQ_VFo

NOTE: If your led strip has either 5v or 12v voltage, I'd recommend using an additional power unit to power the strip from the board. It will grant steady light and won't damage or drain your Pi.


To start led from the console, install `pigpio` and run the service:

Install: https://abyz.me.uk/rpi/pigpio/download.html

```sh 
pip install pigpio
```

Then you can set individual led brightness using 0-255 values:
```sh
pigs p 17 000 # red (off)
pigs p 22 255 # green (on)
pigs p 24 000 # blue (off)
```

To free up GPIO pins set up, kill `pigpiod` service.

#### Command led strip from python

User raspberry GPIO lib:
[gpiozero](https://gpiozero.readthedocs.io/en/latest/index.html)

Video: https://www.youtube.com/watch?v=t3SFYgN2WEc

Example of a python test app:
```py
import gpiozero
from gpiozero import PWMLED
from math import cos, sin
from time import sleep

# PWMLED allow to set brightness percentage

red = PWMLED(17)
green = PWMLED(22)
blue = PWMLED(24)

def shades(x: int = 1):
    for i in range(400):
        green.value = abs(cos(i/10)*x)
        blue.value = abs(sin(i/10)*x)
        red.value = green.value*blue.value*x
        sleep(0.05)

def switch_off():
    red.off()
    green.off()
    blue.off()

if __name__ == '__main__':
    shades()
    switch_off()
```

## Take photos

Raspberry Pi DSLR Camera Control: https://pimylifeup.com/raspberry-pi-dslr-camera-control/

### GPhoto2


```sh
# check if camera is detected
gphoto2 --auto-detect
# check full details
gphoto2 --summary
# take a picture and download it into the Pi
gphoto2 --capture-image-and-download
```

#### libgphoto2 :: supported cameras
http://www.gphoto.org/proj/libgphoto2/support.php

#### Remote controlling cameras
http://www.gphoto.org/doc/remote/

### Olympus cameras

#### C750 UZ

Despite been supported by gphoto2, I couldn't make this work yet.

Error:
```
*** Error ***              
Sorry, your camera does not support generic capture list-config.log gphoto2-debug
ERROR: Could not capture image.
ERROR: Could not capture.
*** Error (-6: 'Unsupported operation') ***
```

#### Olympus OM-D EM I.
If you find some issue, check this out: https://github.com/gphoto/libgphoto2/issues/229


## Print

### Install from the PI

This is a good guide on how to print from the Raspberry PI: https://www.youtube.com/watch?v=jK3rFKajb_Q

### Install driver for dye-sublimation printer

dye-sublimation printer Canon Selphy (117 €). I've bought this one cause I wanted a good quality photos, 
although you need proper drivers to make it work on the PI.
Searching on the web I found that Gutenprint supports lots of dye-subl printers and the Canon is Tier-1 supported (all known features are supported and tested).

link: https://www.peachyphotos.com/blog/stories/dye-sublimation-photo-printers-and-linux/

To proper install the driver, follow this procedure: https://www.peachyphotos.com/blog/stories/building-modern-gutenprint/
Code: 
```sh
# ssh into your pi and type your password or default
ssh pi@<raspberry pi IP address>
# Gain root
sudo su -
### Install pre-requisites
# Remove existing gutenprint packages and ipp-usb
apt remove *gutenprint* ipp-usb
# Install necessary development libraries
apt install libusb-1.0-0-dev libcups2-dev pkg-config
# Install CUPS (just in case)
apt install cups-daemon
# Install git-lfs
apt install git-lfs
### Download and compile Gutenprint
# Download latest gutenprint snapshot from sourceforge
GUTENPRINT_VER=5.3.4-2023-12-06T01-00-2ef8ba24
curl -o gutenprint-${GUTENPRINT_VER}.tar.xz "https://master.dl.sourceforge.net/project/gimp-print/snapshots/gutenprint-${GUTENPRINT_VER}.tar.xz?viasf=1"
# Decompress & Extract
tar -xJf gutenprint-${GUTENPRINT_VER}.tar.xz
# Compile gutenprint
cd gutenprint-${GUTENPRINT_VER}
./configure --without-doc
make -j4
make install
cd ..
# Refresh PPDs
cups-genppdupdate
# Restart CUPS
service cups restart
## At this point you can stop unless you have certian Mitsubishi, Sinfonia, Fujifilm, and Hiti models)
### Download and compile latest backend code
# Get the latest selphy_print code
git clone https://git.shaftnet.org/gitea/slp/selphy_print.git
# Compile selphy_print
cd selphy_print
make -j4 
make install
# Set up library include path
echo "/usr/local/lib" > /etc/ld.so.conf.d/usr-local.conf
ldconfig
# FiN

```


## CUPS

CUPS (formerly an acronym for Common UNIX Printing System) is a modular printing system for Unix-like computer operating systems which allows a computer to act as a print server. A computer running CUPS is a host that can accept print jobs from client computers, process them, and send them to the appropriate printer.

Official page: https://apple.github.io/cups/

Install CUPS:
```sh
sudo apt-get install cups -y
```

The you need to add your pi account (default `pi`) so you are able to add, manage and remove printers:
```sh
# if you're not using the default user "pi", just add your user name
sudo usermode -a -G lpadmin pi
```

To enable cups to access it from remote:
```sh
# enable admin access from remote
sudo cupsctl --remote-admin --remote-any --share-printers
# enable web interface
cupsctl WebInterface=yes
```

Whenever you set up configurations, restart the service
```sh
sudo service cups restart
```

You can view and change full CUPS configuration, VIM into the conf file
```sh
sudo cat /etc/cups/cupsd.conf
```
Here you can change, for example, the default port (631)

Full configuration details: https://www.cups.org/doc/man-cupsd.conf.html

Check if CUPS service is listening on port 631 (or the custom one you have changed):
```sh
netstat -punta
```

To access CUPS web service, open browser and go to the URL : `http://<your-ip-address>:<cups-port>`. Example
```
http://192.168.1.31:631/
```

You can add the printer via USB port to the Pi or connect it to your network if is supports wifi.

https://www.raspberrypi.com/news/printing-at-home-from-your-raspberry-pi/

If it looks that new configs doesn't work, restart the cups service:
```sh
sudo service cups restart
```

Set up your printer: https://github.com/apple/cups?tab=readme-ov-file#setting-up-printer-queues-using-your-web-browser

Do it from the web interface:
Check with guide: https://tutorials-raspberrypi.com/raspberry-pi-printer-setup-and-printing-images-by-pressing-button/

Or follow the instruction in the video: https://youtu.be/jK3rFKajb_Q?si=TZmhOAMuhHVJAjvE&t=124

Run:
```sh
lpstat -p
> printer Canon_SELPHY_CP1500 is idle.  enabled since Fri 22 Mar 2024 22:48:45 GMT
```

NOTE: if `lp` command sends the file to the printer but it fails with the message  "Cannot read data! Cannot print incompatible images or memory card not readable", try to remove and add the printer keeping the default name or add underscores '_' in between strings.


Print:

```sh
# lp -d <printer name> <file name>
lp -d Canon_SELPHY_CP1500 P1010464.JPG
```

## Troubleshooting

### PiBooth

When running `pibooth` it fail out due to detection camera issues:
```
pibooth
pygame 2.5.2 (SDL 2.28.3, Python 3.9.2)
Hello from the pygame community. https://www.pygame.org/contribute.html
pygame-menu 4.0.7
[ INFO    ] pibooth           : Installed plugins:
[ INFO    ] pibooth           : Starting the photo booth application on Raspberry pi 4B
/usr/local/lib/python3.9/dist-packages/pluggy/_manager.py:469: PluggyTeardownRaisedWarning: A plugin raised an exception during an old-style hookwrapper teardown.
Plugin: pibooth-core:camera, Hook: pibooth_setup_camera
OSError: Neither Raspberry Pi nor GPhoto2 nor OpenCV camera detected
For more information see https://pluggy.readthedocs.io/en/stable/api_reference.html#pluggy.PluggyTeardownRaisedWarning
  outcome = Result.from_call(
Traceback (most recent call last):
  File "/usr/local/bin/pibooth", line 8, in <module>
    sys.exit(main())
  File "/usr/local/lib/python3.9/dist-packages/pibooth/booth.py", line 490, in main
    app = PiApplication(config, plugin_manager)
  File "/usr/local/lib/python3.9/dist-packages/pibooth/booth.py", line 131, in __init__
    self.camera = self._pm.hook.pibooth_setup_camera(cfg=self._config)
  File "/usr/local/lib/python3.9/dist-packages/pluggy/_hooks.py", line 501, in __call__
    return self._hookexec(self.name, self._hookimpls.copy(), kwargs, firstresult)
  File "/usr/local/lib/python3.9/dist-packages/pluggy/_manager.py", line 119, in _hookexec
    return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
  File "/usr/local/lib/python3.9/dist-packages/pluggy/_manager.py", line 473, in traced_hookexec
    return outcome.get_result()
  File "/usr/local/lib/python3.9/dist-packages/pluggy/_result.py", line 99, in get_result
    raise exc.with_traceback(exc.__traceback__)
  File "/usr/local/lib/python3.9/dist-packages/pluggy/_result.py", line 61, in from_call
    result = func()
  File "/usr/local/lib/python3.9/dist-packages/pluggy/_manager.py", line 470, in <lambda>
    lambda: oldcall(hook_name, hook_impls, caller_kwargs, firstresult)
  File "/usr/local/lib/python3.9/dist-packages/pluggy/_callers.py", line 155, in _multicall
    teardown[0].send(outcome)
  File "/usr/local/lib/python3.9/dist-packages/pibooth/plugins/camera_plugin.py", line 28, in pibooth_setup_camera
    cam = camera.find_camera()
  File "/usr/local/lib/python3.9/dist-packages/pibooth/camera/__init__.py", line 52, in find_camera
    raise EnvironmentError("Neither Raspberry Pi nor GPhoto2 nor OpenCV camera detected")
OSError: Neither Raspberry Pi nor GPhoto2 nor OpenCV camera detected
```

This might be cause your camera is not connected properly or switched off, **OR** gphoto2 python library doesn't recognize it. See "x   GPhoto2 lib" section.

### GPhoto2 lib

Once you've instsalled [gphoto2 python lib](), might happen that importing it from a python script would result in an import error:

```py
>>> import gphoto2
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/local/lib/python3.9/dist-packages/gphoto2/__init__.py", line 30, in <module>
    from gphoto2.abilities_list import *
  File "/usr/local/lib/python3.9/dist-packages/gphoto2/abilities_list.py", line 10, in <module>
    import gphoto2.port_info_list
  File "/usr/local/lib/python3.9/dist-packages/gphoto2/port_info_list.py", line 10, in <module>
    from ._port_info_list import *
ImportError: /usr/local/lib/python3.9/dist-packages/gphoto2/_port_info_list.cpython-39-aarch64-linux-gnu.so: undefined symbol: gp_port_init_localedir, version LIBGPHOTO2_5_0
```

Seems that current version of `libgphoto2` (the C-based library used to actually build the python gphoto2 lib) doesn't recognize or include `gp_port_init_localedir`. Let's see what is my version

```sh
$ gphoto2 -v
gphoto2 2.5.28

...

This version of gphoto2 is using the following software versions and options:
gphoto2         2.5.28         gcc, popt(m), exif, no cdk, no aa, jpeg, no readline
libgphoto2      2.5.27         standard camlibs, gcc, ltdl, EXIF
libgphoto2_port 0.12.0         iolibs: disk ptpip serial usb1 usbdiskdirect usbscsi, gcc, ltdl, EXIF, USB, serial without locking
```
Ok, I see `libgphoto2` is at v `2.5.27`. 

Looking at the [developer readme](https://github.com/jim-easterbrook/python-gphoto2/tree/284ddac77b91ec325bce9754f5dc867e506f5893/developer) of the python lib (well recommended to read), you can see the change log, as well as other useful stuff. Here's what it list (trail end):

```
...

2.5.30    Add gp_init_localedir & gp_port_init_localedir functions
2.5.31    No change
```

Bingo! `gp_port_init_localedir` has been implemented from v `2.5.30` on.
Now, as the dev guide says, we need to:
> To build python-gphoto2 with a different version of libgphoto2 than the one installed on your system you first need to build a local copy of libgphoto2. [Download and extract the libgphoto2 source](https://sourceforge.net/projects/gphoto/files/libgphoto/), change to the source directory and then configure, build and install

Let's do it then:

```sh
# download the latest version (2.5.31 at the moment of writing)
wget https://sourceforge.net/projects/gphoto/files/libgphoto/2.5.31/libgphoto2-2.5.31.tar.xz

# unzip the archive
tar xf libgphoto2-2.5.31.tar.xz
cd libgphoto2-2.5.31

# Configure lib prior to build
# Note the use of --prefix=$PWD/local_install to create a local copy, rather than a system installation.
./configure --prefix=$PWD/local_install CFLAGS="-std=gnu99 -g -O2"
make
make install

# build and install python package that includes your local copy of the libgphoto2 libs
# The GPHOTO2_ROOT environment variable tells setup.py to use the files in libgphoto2-2.5.31/local_install. This value needs to be an absolute path.
GPHOTO2_ROOT=$PWD/libgphoto2-2.5.31/local_install pip install --user . -v
```

Let's see if it worked:
```sh
$ python
Python 3.9.2 (default, Feb 28 2021, 17:03:44)
[GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> try:
...     import gphoto2
...     print('Yay!')
... except:
...     print('Still no luck :(')
...     raise
...
Yay!
```
# mg-pybooth
MG own photo booth project

# Raspberry Pi

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
pigs p 17 000
pigs p 22 255 # green
pigs p 24 000
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
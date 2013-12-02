### Important Notes

The following steps have been known to work and should be followed from up to bottom.
If you deviate from this guide, do it with caution and make sure you don't violate
any assumptions ProxyPoS makes about its environment. 

#### If you find a bug

If you find a bug/error in this guide please submit an issue or pull request
following the contribution guide (see [README.md](README.md)).

- - -

The ProxyPoS installation consists of setting up the following components:

1. Dependencies
2. ProxyPoS
3. Hardware Setup
4. Install Init Script

----------

## 1. Installing Dependencies
These instructions are proved for Linux Mint, instructions for other flavors of Debian-based distros should be similar.

You will first need to install the following packages:

1. python version >= 2.6
2. At least one of the supported libraries (libusb 1.0, libusb 0.1 or OpenUSB)
3. python imaging, python yaml & setuptools
4. Git get some packages needed

For example, the command:

```$ sudo apt-get install python python-imaging python-setuptools python-yaml libusb-dev git```

should install all these packages on most Debian-based systems with access to the proper package repositories.

### 1. PyUSB
Checkout the latest code from github
Build and install it:

    cd /tmp
    git clone https://github.com/walac/pyusb.git
    cd pyusb
    python setup.py build
    sudo python setup.py install

----------

### 2. python-qrcode
This is the python module to generate QR Codes
Checkout the latest code from github
Build and install it:

    cd /tmp
    git clone https://github.com/lincolnloop/python-qrcode.git
    cd python-qrcode
    python setup.py build
    sudo python setup.py install

----------
    
### 3. python-escpos
This is the python module to communicate with ESC/PoS printers
Checkout the latest code from github
Build and install it:

    cd /tmp
    git clone https://github.com/agb80/python-escpos.git
    cd python-escpos
    python setup.py build
    sudo python setup.py install

----------

## 2. ProxyPoS

### Create user for ProxyPoS

    sudo adduser --system --shell /bin/bash --group dialout --home /home/proxypos/ proxypos
    
We'll install ProxyPoS into home directory of the user `proxypos`:

    # Clone ProxyPoS repository
    cd /home/proxypos
    sudo su - proxypos
    git clone https://github.com/Fedrojesa/ProxyPoS.git proxypos
    
### Configure it
Copy the example ProxyPos config files and customice as you need

    cp proxypos/config/logging.yaml.example config/logging.yaml
    cp proxypos/config/printer.yaml.example config/printer.yaml


### Make executable
Make main script executable

    sudo chmod +x /home/proxypos/proxypos/proxypos-server
    
----------

## 3. Hardware Setup
1. Get the Product ID and Vendor ID from the lsusb command

    lsusb
    Bus 002 Device 001: ID 1a2b:1a2b Device name
    
2. Write the values on the printer.yaml file

    vi /home/proxypos/proxypos/config/printer.yaml

3. Create a udev rule to let users belonging to dialout group use the printer. 
You can create the file /etc/udev/rules.d/99-escpos.rules and add the following:

    SUBSYSTEM=="usb", ATTRS{idVendor}=="1a2b", ATTRS{idProduct}=="1a2b", MODE="0664", GROUP="dialout"
    
Replace idVendor and idProduct hex numbers with the ones that you got from the step #1. 

4. Restart udev

    sudo udevadm trigger
    sudo service udev restart
    
## 4. Install Init Script

Move the init script to  /etc/init.d/proxypos:

    sudo cp /home/proxypos/proxypos/init/sysvinit/ubuntu/proxypos /etc/init.d/
    sudo chmod +x /etc/init.d/proxypos
    sudo chown root: /etc/init.d/proxypos

Make ProxyPoS start on boot:

    sudo update-rc.d proxypos defaults
    
Create directory for log files and set permissions

    sudo mkdir /var/log/proxypos
    sudo chown proxypos:root /var/log/proxypos
    
Start your ProxyPoS instance:

    sudo /etc/init.d/proxypos start
    
# ProxyPoS

ProsyPoS is a software to use as a driver for PoS devices to use with OpenERP PoS module.
It is on early development status, we are going to continue workgint on it
as our customer required. 

If you need a feature that is not currently supported, contactme at atin81@gmail.com
and consider make a donation for speed up development process.

All contributions are welcome, just see Contributing section for general guide lines.

## Features

* USB PoS printter support

## Dependencies

In order to start getting access to your printer, you must ensure 
you have previously installed the following python modules:

* python-escpos (https://code.google.com/p/python-escpos/)

## Installation

1. Basic installation
------------------------------------------------------------------

As currently is building on top of OpenERP server, 
follow guidelines for basic OpenERP installation.


2. Define your printer
------------------------------------------------------------------

Before start use driver, you must see at your system for the printer 
parameters. This is done with the 'lsusb' command.

First run the command to look for the "Vendor ID" and "Product ID",
then write down the values, these values are displayed just before
the name of the device with the following format:

    xxxx:xxxx

Example:
  Bus 002 Device 001: ID 1a2b:1a2b Device name

Then look for the file devices.cfg on folder addons/point_of_sale/controllers/
and write down the the values in question.

  [printer]
  idVendor = 0x0483
  idProduct = 0x5740


## TODO:

1. Add support for templates on receipts
2. Add support for Barcode Reader
3. Add support for Electronic Balance
4. GUI for know current status & configuration
5. Simplify installation

## Contributing

* Check out the latest master to make sure the feature hasn't been implemented or the bug hasn't been fixed yet
* Check out the issue tracker to make sure someone already hasn't requested it and/or contributed it
* Fork the project
* Start a feature/bugfix branch
* Commit and push until you are happy with your contribution
* Please try not to mess with the version, or history. If you want to have your own version, or is otherwise necessary, that is fine,
  but please isolate to its own commit so I can cherry-pick around it.
  
## Copyright

Copyright (c) 2013 Agustín Cruz. See LICENSE for further details.

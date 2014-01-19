# ProxyPoS

ProsyPoS is a software to use as a driver for PoS devices to use with OpenERP PoS module.
It is on early development status, we are going to continue workgint on it
as our customer required. 

If you need a feature that is not currently supported, contactme at atin81@gmail.com
and consider make a donation for speed up development process.

All contributions are welcome, just see Contributing section for general guide lines.

## Features

* USB PoS printter support
* Serial PoS printter support

## Dependencies & Installation
------------------------------------------------------------------

[Installation instructions](INSTALL.md)


## Sales Receipt Customization
------------------------------------------------------------------

At the momment there is no support for custom receipts templates,
we are currently working on to add this feature. 
The easy way to customize the receipts is directly editing the
```print_receipt``` function on proxypos/controlers/printer.py


## Supported Hardware
------------------------------------------------------------------

The system has been testing successfully working on LinuxMint 13
with following ESCPoS printers:

* EC 5894 - EC Line
* EC 5890X - EC Line
* TMU-220D - Epson


## TODO:

1. ~~Simplify the app using different webserver than the OE web module~~
2. Add support for templates on receipts
3. Merge with https://github.com/diassynthesis/OpenERP-ledDisplay
4. Add support for Barcode Reader
5. Add support for Electronic Balance
6. GUI for know current status & configuration

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

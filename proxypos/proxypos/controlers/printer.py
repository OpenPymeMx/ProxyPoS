# -*- encoding: utf-8 -*-
###########################################################################
#  Copyright (c) 2013 OpenPyme - http://www.openpyme.mx/
#  All Rights Reserved.
#  Coded by: Agustín Cruz Lozano (agustin.cruz@openpyme.mx)
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.
#
##############################################################################

import logging
from escpos import printer

logger = logging.getLogger(__name__)


def open_cashbox():
    from proxypos.proxypos import config
    # Init printer
    ptype = config.get('printer.type').lower()
    settings = config.get('printer.settings')
    idVendor = settings['idVendor']
    idProduct = settings['idProduct']
    if ptype == 'usb':
        with printer.Usb(idVendor, idProduct) as device:
            device.cashdraw(2)
    elif ptype == 'serial':
        # TODO:
        printer.Serial(settings['devfile'])
    elif ptype == 'network':
        # TODO:
        printer.Network(settings['host'])


def print_receipt(receipt):
    """ Function used for print the receipt
    """
    # Import configuration handler
    from proxypos.proxypos import config
    from proxypos.proxypos import tmphandler

    # Init printer
    ptype = config.get('printer.type').lower()
    settings = config.get('printer.settings')
    idVendor = settings['idVendor']
    idProduct = settings['idProduct']
    if ptype == 'usb':
        with printer.Usb(idVendor, idProduct) as device:
            # Assign other default values
            device.pxWidth = settings['pxWidth']
            # Set default widht with normal value
            device.width = device.widthA = settings['WidthA']
            device.widthB = settings['WidthB']
            # Set correct table character
            if 'charSet' in settings:
                device.text(settings['charSet'])
            template = config.get('receipt.template')
            # Render and print receipt
            tmphandler.print_receipt(device, template, receipt)
    elif ptype == 'serial':
        # TODO:
        printer.Serial(settings['devfile'])
    elif ptype == 'network':
        # TODO:
        printer.Network(settings['host'])


def is_alive():
    from proxypos.proxypos import config
    # Init printer
    ptype = config.get('printer.type').lower()
    settings = config.get('printer.settings')
    idVendor = settings['idVendor']
    idProduct = settings['idProduct']
    if ptype == 'usb':
        with printer.Usb(idVendor, idProduct) as device:
            pass
    elif ptype == 'serial':
        # TODO:
        printer.Serial(settings['devfile'])
    elif ptype == 'network':
        # TODO:
        printer.Network(settings['host'])

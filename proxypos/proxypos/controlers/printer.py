# -*- encoding: utf-8 -*-
###########################################################################
#    Copyright (c) 2013 OpenPyme - http://www.openpyme.mx/
#    All Rights Reserved.
#    Coded by: Agustín Cruz Lozano (agustin.cruz@openpyme.mx)
#
#    Permission is hereby granted, free of charge, to any person obtaining a copy
#    of this software and associated documentation files (the "Software"), to deal
#    in the Software without restriction, including without limitation the rights
#    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#    copies of the Software, and to permit persons to whom the Software is
#    furnished to do so, subject to the following conditions:
#
#    The above copyright notice and this permission notice shall be included in
#    all copies or substantial portions of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#    THE SOFTWARE.
#
##############################################################################

import logging
from escpos import printer

logger = logging.getLogger(__name__)

class device:
    """ ESC/POS device object """

    def __init__(self):
        """Setup printer configuration

        """
        # Import configuration handler
        from proxypos.proxypos import config
        # Init printer
        ptype = config.get('printer.type').lower()
        settings = config.get('printer.settings')
        if ptype == 'usb':
            self.printer = printer.Usb(settings['idVendor'],
                                       settings['idProduct'])
        elif ptype == 'serial':
            self.printer = printer.Serial(settings['devfile'])
        elif ptype == 'network':
            self.printer = printer.Network(settings['host'])
        # Assign other default values
        self.printer.pxWidth = settings['pxWidth']
        # Set default widht with normal value
        self.printer.width = self.printer.widthA = settings['WidthA']
        self.printer.widthB = settings['WidthB']
        # Set correct table character
        if 'charSet' in settings:
            self.printer.text(settings['charSet'])


    def open_cashbox(self):
        self.printer.cashdraw(2)


    def print_receipt(self, receipt):
        """ Function used for print the recipt, currently is the only
        place where you can customize your printout.
        """
        # Import configuration handler
        from proxypos.proxypos import config
        from proxypos.proxypos import tmphandler

        template = config.get('receipt.template')

        # Render and print receipt
        tmphandler.print_receipt(self, template, receipt)


    # Helper functions to facilitate printing
    def _format_date(self, date):
        string = str(date['date']) + '/' + str(date['month']) + '/' + str(date['year']) + ' ' + str(date['hour']) + ':' + "%02d" % date['minute']
        return string

    def _write(self, string, rcolstr=None, align="left"):
        """Write simple text string. Remember \n for newline where applicable.
        rcolstr is a righthand column that may be added
        (e.g. a price on a receipt). Be aware that when rcolstr is
        used newline(s) may only be a part of rcolstr, and only as
        the last character(s)."""
        if align != "left" and len(string) < self.printer.width:
            blanks = 0
            if align == "right":
                blanks = self.printer.width - len(string.rstrip("\n"))
            if align == "center":
                blanks = (self.printer.width - len(string.rstrip("\n"))) / 2
            string = " " * blanks + string

        if not rcolstr:
            try:
                self.printer.text(string)
            except:
                logger.error('No pude escribir', exc_info=1)
                raise
        else:
            rcolStrRstripNewline = rcolstr.rstrip("\n")
            if "\n" in string or "\n" in rcolStrRstripNewline:
                raise ValueError("When using rcolstr in POSprinter.write only newline at the end of rcolstr is allowed and not in string (the main text string) it self.")
            # expand string
            lastLineLen = len(string) % self.printer.width + len(rcolStrRstripNewline)
            if lastLineLen > self.printer.width:
                numOfBlanks = (self.printer.width - lastLineLen) % self.printer.width
                string += numOfBlanks * " "
                lastLineLen = len(string) % self.printer.width + len(rcolStrRstripNewline)
            if lastLineLen < self.printer.width:
                numOfBlanks = self.printer.width - lastLineLen
                string += " " * numOfBlanks
            try:
                self.printer.text(string + rcolstr)
            except:
                logger.error('No pude escribir', exc_info=1)
                raise

    def _lineFeed(self, times=1, cut=False):
        """Write newlines and optional cut paper"""
        while times:
            try:
                self.printer.text("\n")
            except:
                raise
            times -= 1
        if cut:
            try:
                self.printer.cut('part')
            except:
                raise

    def lineFeedCut(self, times=6, cut=True):
        """Enough line feed for the cut to be beneath the previously printed text etc."""
        try:
            self._lineFeed(times, cut)
        except:
            raise

    def _font(self, font='a'):
        if font == 'a':
            self.printer._raw('\x1b\x4d\x01')
            self.printer.width = self.printer.widthA
        else:
            self.printer._raw('\x1b\x4d\x00')
            self.printer.width = self.printer.widthB

    def _bold(self, bold=True):
        if bold:
            self.printer._raw('\x1b\x45\x01')
        else:
            self.printer._raw('\x1b\x45\x00')

    def _decimal(self, number):
        return "%0.2f" % float(number)

    def _printImgFromFile(self, filename, resolution="high", align="center", scale=None):
        """Print an image from a file.
        resolution may be set to "high" or "low". Setting it to low makes the image a bit narrow (90x60dpi instead of 180x180 dpi) unless scale is also set.
        align may be set to "left", "center" or "right".
        scale resizes the image with that factor, where 1.0 is the full width of the paper."""
        try:
            from PIL import Image
            # Open file and convert to black/white (colour depth of 1 bit)
            img = Image.open(filename).convert("1")
            self._printImgFromPILObject(img, resolution, align, scale)
        except:
            raise

    def _printImgFromPILObject(self, imgObject, resolution="high", align="center", scale=None):
        """The object must be a Python ImageLibrary object, and the colordepth should be set to 1."""
        try:
            # If a scaling factor has been indicated
            if scale:
                assert type(scale) == float
                if scale > 1.0 or scale <= 0.0:
                    raise ValueError, "scale: Scaling factor must be larger than 0.0 and maximum 1.0"
                # Give a consistent output regardless of the resolution setting
                scale *= self.printer.pxWidth / float(imgObject.size[0])
                if resolution is "high":
                    scaleTuple = (scale * 2, scale * 2)
                else:
                    scaleTuple = (scale, scale * 2 / 3.0)
                # Convert to binary colour depth and resize
                imgObjectB = imgObject.resize([ int(scaleTuple[i] * imgObject.size[i]) for i in range(2) ]).convert("1")
            else:
                # Convert to binary colour depth
                imgObjectB = imgObject.convert("1")
            # Convert to a pixel access object
            imgMatrix = imgObjectB.load()
            width = imgObjectB.size[0]
            height = imgObjectB.size[1]
            # Print it
            self._printImgMatrix(imgMatrix, width, height, resolution, align)
        except:
            raise

    def _printImgMatrix(self, imgMatrix, width, height, resolution, align):
        """Print an image as a pixel access object with binary colour."""
        if resolution == "high":
            scaling = 24
            currentpxWidth = self.printer.pxWidth * 2
        else:
            scaling = 8
            currentpxWidth = self.printer.pxWidth
        if width > currentpxWidth:
            raise ValueError("Image too wide. Maximum width is configured to be " + str(currentpxWidth) + "pixels. The image is " + str(width) + " pixels wide.")
        tmp = ''
        for yScale in range(-(-height / scaling)):
            # Set mode to hex and 8-dot single density (60 dpi).
            if resolution == "high":
                outList = [ "0x1B", "0x2A", "0x21" ]
            else:
                outList = [ "0x1B", "0x2A", "0x00" ]
            # Add width to the communication to the printer. Depending on the alignment we count that in and add blank vertical lines to the outList
            if align == "left":
                blanks = 0
            if align == "center":
                blanks = (currentpxWidth - width) / 2
            if align == "right":
                blanks = currentpxWidth - width
            highByte = (width + blanks) / 256
            lowByte = (width + blanks) % 256
            outList.append(hex(lowByte))
            outList.append(hex(highByte))
            if resolution == "high":
                blanks *= 3
            if align == "left":
                pass
            if align == "center":
                for i in range(blanks):
                    outList.append(hex(0))
            if align == "right":
                for i in range(blanks):
                    outList.append(hex(0))
            for x in range(width):
                # Compute hex string for one vertical bar of 8 dots (zero padded from the bottom if necessary).
                binStr = ""
                for y in range(scaling):
                    # Indirect zero padding. Do not try to extract values from images beyond its size.
                    if (yScale * scaling + y) < height:
                        binStr += "0" if imgMatrix[x, yScale * scaling + y] == 255 else "1"
                    # Zero padding
                    else:
                        binStr += "0"
                outList.append(hex(int(binStr[0:8], 2)))
                if resolution == "high":
                    outList.append(hex(int(binStr[8:16], 2)))
                    outList.append(hex(int(binStr[16:24], 2)))
            for element in outList:
                try:
                    tmp += chr(int(element, 16))
                except:
                    raise

        self._write(tmp)

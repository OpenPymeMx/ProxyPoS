# -*- coding: utf-8 -*-
from ConfigParser import SafeConfigParser
import logging
import simplejson
import os
import io
import openerp
from escpos import *

from openerp.addons.web.controllers.main import manifest_list, module_boot, html_template

class PointOfSaleController(openerp.addons.web.http.Controller):
    _cp_path = '/pos'

    @openerp.addons.web.http.httprequest
    def app(self, req, s_action = None, **kw):
        js = "\n        ".join('<script type="text/javascript" src="%s"></script>' % i for i in manifest_list(req, None, 'js'))
        css = "\n        ".join('<link rel="stylesheet" href="%s">' % i for i in manifest_list(req, None, 'css'))

        cookie = req.httprequest.cookies.get("instance0|session_id")
        session_id = cookie.replace("%22", "")
        template = html_template.replace('<html', '<html manifest="/pos/manifest?session_id=%s"' % session_id)
        r = template % {
            'js': js,
            'css': css,
            'modules': simplejson.dumps(module_boot(req)),
            'init': 'var wc = new s.web.WebClient();wc.appendTo($(document.body));'
        }
        return r

    @openerp.addons.web.http.httprequest
    def manifest(self, req, **kwargs):
        """ This generates a HTML5 cache manifest files that preloads the categories and products thumbnails 
            and other ressources necessary for the point of sale to work offline """

        ml = ["CACHE MANIFEST"]

        # loading all the images in the static/src/img/* directories
        def load_css_img(srcdir, dstdir):
            for f in os.listdir(srcdir):
                path = os.path.join(srcdir, f)
                dstpath = os.path.join(dstdir, f)
                if os.path.isdir(path) :
                    load_css_img(path, dstpath)
                elif f.endswith(('.png', '.PNG', '.jpg', '.JPG', '.jpeg', '.JPEG', '.gif', '.GIF')):
                    ml.append(dstpath)

        imgdir = openerp.modules.get_module_resource('point_of_sale', 'static/src/img');
        load_css_img(imgdir, '/point_of_sale/static/src/img')

        products = req.session.model('product.product')
        for p in products.search_read([('pos_categ_id', '!=', False)], ['name']):
            product_id = p['id']
            url = "/web/binary/image?session_id=%s&model=product.product&field=image&id=%s" % (req.session_id, product_id)
            ml.append(url)

        categories = req.session.model('pos.category')
        for c in categories.search_read([], ['name']):
            category_id = c['id']
            url = "/web/binary/image?session_id=%s&model=pos.category&field=image&id=%s" % (req.session_id, category_id)
            ml.append(url)

        ml += ["NETWORK:", "*"]
        m = "\n".join(ml)

        return m

    @openerp.addons.web.http.jsonrequest
    def dispatch(self, request, iface, **kwargs):
        method = 'iface_%s' % iface
        return getattr(self, method)(request, **kwargs)

    @openerp.addons.web.http.jsonrequest
    def scan_item_success(self, request, ean):
        """
        A product has been scanned with success
        """
        print 'scan_item_success: ' + str(ean)
        return

    @openerp.addons.web.http.jsonrequest
    def scan_item_error_unrecognized(self, request, ean):
        """
        A product has been scanned without success
        """
        print 'scan_item_error_unrecognized: ' + str(ean)
        return

    @openerp.addons.web.http.jsonrequest
    def keypad_item_success(self, request, data):
        """
        A product has been entered by keypad with success
        """
        print 'keypad_item_success: ' + str(data)
        return

    @openerp.addons.web.http.jsonrequest
    def keypad_item_error_unrecognized(self, request, data):
        """
        A product has been entered by keypad without success
        """
        print 'keypad_item_error_unrecognized: ' + str(data)
        return

    @openerp.addons.web.http.jsonrequest
    def help_needed(self, request):
        """
        The user wants an help (ex: light is on)
        """
        print "help_needed"
        return

    @openerp.addons.web.http.jsonrequest
    def help_canceled(self, request):
        """
        The user stops the help request
        """
        print "help_canceled"
        return

    @openerp.addons.web.http.jsonrequest
    def weighting_start(self, request):
        print "weighting_start"
        return

    @openerp.addons.web.http.jsonrequest
    def weighting_read_kg(self, request):
        print "weighting_read_kg"
        return 0.0

    @openerp.addons.web.http.jsonrequest
    def weighting_end(self, request):
        print "weighting_end"
        return

    @openerp.addons.web.http.jsonrequest
    def payment_request(self, request, price):
        """
        The PoS will activate the method payment 
        """
        print "payment_request: price:" + str(price)
        return 'ok'

    @openerp.addons.web.http.jsonrequest
    def payment_status(self, request):
        print "payment_status"
        return { 'status':'waiting' }

    @openerp.addons.web.http.jsonrequest
    def payment_cancel(self, request):
        print "payment_cancel"
        return

    @openerp.addons.web.http.jsonrequest
    def transaction_start(self, request):
        print 'transaction_start'
        return

    @openerp.addons.web.http.jsonrequest
    def transaction_end(self, request):
        print 'transaction_end'
        return

    @openerp.addons.web.http.jsonrequest
    def cashier_mode_activated(self, request):
        print 'cashier_mode_activated'
        return

    @openerp.addons.web.http.jsonrequest
    def cashier_mode_deactivated(self, request):
        print 'cashier_mode_deactivated'
        return

    @openerp.addons.web.http.jsonrequest
    def open_cashbox(self, request):
        # print 'open_cashbox'
        self._init_printer()
        self.printer.cashdraw(2)
        return

    @openerp.addons.web.http.jsonrequest
    def print_receipt(self, request, receipt):
        """
        The user send a receipt to print
        """
        # print 'print_receipt'
        self._print_receipt(receipt)
        return

    @openerp.addons.web.http.jsonrequest
    def print_pdf_invoice(self, request, pdfinvoice):
        print 'print_pdf_invoice' + str(pdfinvoice)
        return

    def _print_receipt(self, receipt):
        self._init_printer()
        path = os.path.dirname(__file__)

        filename = path + '/logo.jpg'

        self.printer.pxWidth = 206

        self._printImgFromFile(filename)

        date = self._format_date(receipt['date'])
        self._bold(False)
        self._font('a')
        self._lineFeed(1)
        self._write(date, None, 'right')
        self._lineFeed(1)
        self._write(receipt['name'] + '\n', '', 'right')

        self._write(receipt['company']['name'] + '\n')
        self._write('RFC: ' + str(receipt['company']['company_registry']) + '\n')
        self._write('Telefono: ' + str(receipt['company']['phone']) + '\n')
        self._write('Cajero: ' + str(receipt['cashier']) + '\n')
        # self._write('Tienda: ' + receipt['store']['name'])
        self._lineFeed(1)
        for line in receipt['orderlines']:
            left = str(line['quantity']) + ' ' + str(line['unit_name']) + ' ' + str(line['product_name'])
            right = self._decimal(line['price_with_tax'])
            self._write(left, right)
            self._lineFeed(1)

        self._lineFeed(2)
        self._write('Subtotal:', self._decimal(receipt['total_without_tax']) + '\n')
        self._write('IVA:', self._decimal(receipt['total_tax']) + '\n')
        self._write('Descuento:', self._decimal(receipt['total_discount']) + '\n')
        self._bold(True)
        self._font('b')
        self._write('TOTAL:', '$' + self._decimal(receipt['total_with_tax']) + '\n')

        # Set space for display payment methods
        self._lineFeed(1)
        self._font('a')
        self._bold(False)
        for payment in receipt['paymentlines']:
            self._write(payment['journal'], self._decimal(payment['amount']))

        self._bold(True)
        self._write('Cambio:', '$ ' + self._decimal(receipt['change']))

        # Footer space
        self._lineFeed(2)
        self._bold(False)
        self._write('GRACIAS POR SU COMPRA', '', 'center')
        self._lineFeedCut(1, True)

    def _init_printer(self):
        """ Init pos printer
        """
        rdy = False

        if hasattr(self, 'printer'):
            try:
                self.printer.hw('INIT')
                rdy = True
            except:
                self.printer = None

        if not rdy:
            parser = SafeConfigParser()
            path = os.path.dirname(__file__)
            parser.read(path + '/devices.cfg')

            for section_name in parser.sections():
                if section_name == 'printer':
                    config = {}
                    for name, value in parser.items(section_name):
                        config[name] = value
            self.printer = printer.Usb(int(config['idvendor'], 16),
                                       int(config['idproduct'], 16))

    # Helper functions to facilitate printing
    def _format_date(self, date):
        string = str(date['date']) + '/' + str(date['month']) + '/' + str(date['year']) + ' ' + str(date['hour']) + ':' + "%02d" % date['minute']
        return string

    def _write(self, string, rcolStr = None, align = "left"):
        """Write simple text string. Remember \n for newline where applicable.
        rcolStr is a righthand column that may be added (e.g. a price on a receipt). 
        Be aware that when rcolStr is used newline(s) may only be a part of rcolStr, 
        and only as the last character(s)."""
        if align != "left" and len(string) < self.printer.width:
            blanks = 0
            if align == "right":
                blanks = self.printer.width - len(string.rstrip("\n"))
            if align == "center":
                blanks = (self.printer.width - len(string.rstrip("\n"))) / 2
            string = " " * blanks + string

        if not rcolStr:
            try:
                self.printer.text(str(string))
            except:
                print 'No pude escribir'
                raise
        else:
            rcolStrRstripNewline = rcolStr.rstrip("\n")
            if "\n" in string or "\n" in rcolStrRstripNewline:
                raise ValueError("When using rcolStr in POSprinter.write only newline at the end of rcolStr is allowed and not in string (the main text string) it self.")
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
                self.printer.text(string + rcolStr)
            except:
                raise

    def _lineFeed(self, times = 1, cut = False):
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

    def _lineFeedCut(self, times = 6, cut = True):
            """Enough line feed for the cut to be beneath the previously printed text etc."""
            try:
                self._lineFeed(times, cut)
            except:
                raise

    def _font(self, font = 'a'):
        if font == 'a':
            self.printer._raw('\x1b\x4d\x01')
            self.printer.width = 42
        else:
            self.printer._raw('\x1b\x4d\x00')
            self.printer.width = 32

    def _bold(self, bold = True):
        if bold:
            self.printer._raw('\x1b\x45\x01')
        else:
            self.printer._raw('\x1b\x45\x00')

    def _decimal(self, number):
        return "%0.2f" % int(number)

    def _printImgFromFile(self, filename, resolution = "high", align = "center", scale = None):
        """Print an image from a file.
        resolution may be set to "high" or "low". Setting it to low makes the image a bit narrow (90x60dpi instead of 180x180 dpi) unless scale is also set.
        align may be set to "left", "center" or "right".
        scale resizes the image with that factor, where 1.0 is the full width of the paper."""
        try:
            import Image
            # Open file and convert to black/white (colour depth of 1 bit)
            img = Image.open(filename).convert("1")
            self._printImgFromPILObject(img, resolution, align, scale)
        except:
            raise

    def _printImgFromPILObject(self, imgObject, resolution = "high", align = "center", scale = None):
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

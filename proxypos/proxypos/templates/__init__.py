# -*- encoding: utf-8 -*-
###########################################################################
#    Copyright (c) 2014 OpenPyme - http://www.openpyme.mx/
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

import os

mapping = {
    "order_name":lambda r: r['name'],
    "total_tax": lambda r: r['total_tax'],
    "shop_name": lambda r: r['shop']['name'],
    "company_name": lambda r: r['company']['name'],
    "company_website": lambda r: r['company']['website'],
    "company_phone": lambda r: r['company']['phone'],
    "company_email": lambda r: r['company']['email'],
    "company_address":lambda r: r['company']['contact_address'],
    "company_vat": lambda r: r['company']['vat'],
    "company_registry": lambda r: r['company']['company_registry'],
    "orderlines": lambda r: r['orderlines'],
    "cashier": lambda r: r['cashier'],
    "client": lambda r: r['client'],
    "currency": lambda r: r['currency'],
    "total_discount": lambda r: r['total_discount'],
    "total_without_tax": lambda r: r['total_without_tax'],
    "invoice_id": lambda r: r['invoice_id'],
    "date": lambda r: r['date'],
    "total_paid": lambda r: r['total_paid'],
    "paymentlines": lambda r: r['paymentlines'],
    "payment_amount": lambda r: r['paymentlines'][0]['amount'],
    "payment_journal": lambda r: r['paymentlines'][0]['journal'],
    "total_with_tax": lambda r: r["total_with_tax"],
    "subtotal": lambda r: r['subtotal'],
    "change": lambda r: r['change'],
    "nineteen_tax": lambda r: r['nineteen_tax'],
    "seven_tax": lambda r: r['seven_tax'],
}

txt_function_mapping = {
    # 'image': lambda printer: printer.printImgFromFile,
    'image': lambda printer: printer.image,
    'font': lambda printer: printer.font,
    'bold': lambda printer: printer.bold,
    'linefeed': lambda printer: printer.lineFeed,
    'write': lambda printer: printer.write,
    'formatdate': lambda printer: printer.format_date,
    'cut':lambda printer: printer.lineFeedCut,
    'decimal': lambda printer: printer.decimal,
    'barcode': lambda printer: printer.barcode,
}


class Template(object):
    def __init__(self, path=None):
        self.templates = dict()

        # Add default template
        self.templates['default'] = os.path.join(os.path.dirname(__file__),
                                                 'default.tmp'
                                                 )
        if path:
            for template in self._find_templates(path):
                f = path + "/" + template + ".tmp"
                self.templates[template] = f

    def _find_templates(self, path):
        try:
            return [f[:-4] for f in os.listdir(path) if f.endswith('.tmp')]
        except OSError:
            return []

    def print_receipt(self, printer, template='default', receipt=None):
        """
        Print the receipt with current template
        """
        from jinja2 import Template
        if receipt == None:
            return
        f = open(self.templates[template]).read()
        tmp = Template(f)
        # Make visible mapping functions inside the jinja2 templates
        for func in mapping:
            tmp.globals[func] = mapping[func](receipt)
        for func in txt_function_mapping:
            tmp.globals[func] = txt_function_mapping[func](printer)
        tmp.globals['str'] = str
        # Print the ticket
        tmp.render()

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
import simplejson as json

from bottle import Bottle, request
from controlers import printer


# Helper funciont to process json request
def _get_data(param=None):
    jsonrpc = request.GET.get('r')
    return json.loads(jsonrpc)['params'][param]

# Main web app
app = Bottle()

# Init logger
logger = logging.getLogger(__name__)

@app.route('/pos/scan_item_success')
def scan_item_success(ean=None):
    """
    A product has been scanned with success
    """
    logger.info('scan_item_success: %s', str(ean))
    return

@app.route('/pos/scan_item_error_unrecognized')
def scan_item_error_unrecognized(ean=None):
    """
    A product has been scanned without success
    """
    logger.info('scan_item_error_unrecognized: %s', str(ean))
    return

@app.route('/pos/weighting_start')
def weighting_start():
    logger.info("weighting_start")
    return

@app.route("/pos/weighting_end")
def weighting_end():
    logger.info("weighting_end")
    return

@app.route('/pos/weighting_read_kg')
def weighting_read_kg():
    return json.dumps(0.0)

@app.route('/pos_keypad_item_success')
def keypad_item_success(data=None):
    """
    A product has been entered by keypad with success
    """
    logger.info('keypad_item_success: %s', str(data))
    return

@app.route('/pos/keypad_item_error_unrecognized')
def keypad_item_error_unrecognized(data=None):
    """
    A product has been entered by keypad without success
    """
    logger.info('keypad_item_error_unrecognized: %s', str(data))
    return

@app.route('/pos/help_needed')
def help_needed():
    """
    The user wants an help (ex: light is on)
    """
    logger.info("help_needed")
    return

@app.route('/pos/help_canceled')
def help_canceled():
    """
    The user stops the help request
    """
    logger.info("help_canceled")
    return

@app.route('/pos/payment_request')
def payment_request(price=None):
    """
    The PoS will activate the method payment 
    """
    logger.info("payment_request: price: %s", str(price))
    return 'ok'

@app.route('/pos/payment_status')
def payment_status():
    logger.info("payment_status")
    return { 'status':'waiting' }

@app.route('/pos/payment_cancel')
def payment_cancel():
    logger.info("payment_cancel")
    return

@app.route('/pos/transaction_start')
def transaction_start():
    logger.info('transaction_start')
    return

@app.route('/pos/transaction_end')
def transaction_end():
    logger.info('transaction_end')
    return

@app.route('/pos/cashier_mode_activated')
def cashier_mode_activated():
    logger.info('cashier_mode_activated')
    return

@app.route('/pos/cashier_mode_deactivated')
def cashier_mode_deactivated():
    logger.info('cashier_mode_deactivated')
    return

@app.route('/pos/open_cashbox')
def open_cashbox():
    logger.info('open_cashbox')
    try:
        device = printer.device()
        device.open_cashbox()
    except (SystemExit, KeyboardInterrupt):
        raise
    except Exception, e:
        logger.error('Failed to open the cashbox', exc_info=True)
    return

@app.route('/pos/print_receipt')
def print_receipt():
    receipt = _get_data('receipt')
    logger.info('Print receipt %s', str(receipt))
    try:
        device = printer.device()
        device.print_receipt(receipt)
    except (SystemExit, KeyboardInterrupt):
        raise
    except Exception, e:
        logger.error('Failed to print receipt', exc_info=True)
    return

@app.route('/pos/print_pdf_invoice')
def print_pdf_invoice():
    pdfinvoice = _get_data('pdfinvoice')
    logger.info('print_pdf_invoice %s', str(pdfinvoice))
    return

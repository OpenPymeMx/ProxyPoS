# -*- coding: utf-8 -*-
import logging
import simplejson as json

from bottle import Bottle, request

# Helper funciont to process json request
def _get_data(param=None):
    jsonrpc = request.GET.get('r')
    return json.loads(jsonrpc)['params'][param]

# Main web app
app = Bottle()
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
    # self._init_printer()
    # self.printer.cashdraw(2)
    return

@app.route('/pos/print_receipt')
def print_receipt():
    receipt = _get_data('receipt')
    logger.info('Print receipt %s', str(receipt))
    # self._print_receipt(receipt)
    return

@app.route('/pos/print_pdf_invoice')
def print_pdf_invoice():
    pdfinvoice = _get_data('pdfinvoice')
    logger.info('print_pdf_invoice %s', str(pdfinvoice))
    return

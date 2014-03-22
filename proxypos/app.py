# -*- encoding: utf-8 -*-
###########################################################################
#  Copyright (c) 2013 OpenPyme - http://www.openpyme.mx/
#  All Rights Reserved.
#  Coded by: Agustín Cruz Lozano (agustin.cruz@openpyme.mx)
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software") to deal
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
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.
#
##############################################################################

import logging
import simplejson as json

from proxypos.bottle import Bottle, request, response
from proxypos.controlers import printer


# This decorator will enable bottle to automatically enable CORS
# on all request so we could handle jquery communication
def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        # set CORS headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

        if request.method != 'OPTIONS':
            # actual request; reply with the actual response
            return fn(*args, **kwargs)

    return _enable_cors


# Main web app
app = Bottle()

# Init logger
logger = logging.getLogger(__name__)


# Helper function to actually print the receipt
def do_print(receipt):
    logger.info('Print receipt %s', str(receipt))
    try:
        device = printer.device()
        device.print_receipt(receipt)
    except (SystemExit, KeyboardInterrupt):
        raise
    except Exception:
        logger.error('Failed to print receipt', exc_info=True)


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
    return json.dumps('ok')


@app.route('/pos/payment_status')
def payment_status():
    logger.info("payment_status")
    return {'status': 'waiting'}


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


@app.route('/pos/is_alive')
@enable_cors
def is_alive():
    """
    Test if printer is connected
    """
    params = dict(request.params)
    logger.debug('Testing printer connection....')
    result = 'ok'
    try:
        printer.device()
    except:
        result = 'no'

    logger.debug('params: %s' % str(params))
    # Getting jquery id
    jquery = params['jsonp']
    answer = '%s({"result": "%s"});' % (jquery, result)

    # Set response as json
    response.headers['Content-type'] = 'application/json'
    return answer


@app.route('/pos/open_cashbox')
def open_cashbox():
    """
    Open the cash box
    """
    logger.info('open_cashbox')
    try:
        device = printer.device()
        device.open_cashbox()
    except (SystemExit, KeyboardInterrupt):
        raise
    except Exception:
        logger.error('Failed to open the cashbox', exc_info=True)
    return


@app.get('/pos/print_receipt')
def print_receipt():
    """
    Receipt send to print using GET method
    """
    logger.info('Procesing /pos/print_receipt GET method')
    params = dict(request.params)
    try:
        logger.debug('Params %s', str(params['r']))
        receipt = json.loads(params['r'])['params']['receipt']
        do_print(receipt)
    except:
        # TODO: If a flag is set could delete this except
        logger.info('Already printed receipt by POST method')
    return


@app.post('/pos/print_receipt')
def print_receipt_post():
    """
    Receipt send to print using the POST method
    """
    logger.info('Procesing /pos/print_receipt POST method')
    params = dict(request.params)
    logger.debug('Params %s', str(params['r']))
    receipt = json.loads(params['r'])['params']['receipt']
    do_print(receipt)
    return


@app.route('/pos/print_pdf_invoice')
def print_pdf_invoice():
    logger.info('print_pdf_invoice')
    return

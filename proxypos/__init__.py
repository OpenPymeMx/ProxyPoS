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

import os
import logging.config

from proxypos.bottle import run
from proxypos.app import app
from proxypos import kaptan

# Init config handler
config = kaptan.Kaptan(handler="yaml")


def main():
    # Set default configuration
    port = '8069'
    host = 'localhost'
    path = 'config/proxypos.yaml'

    # Read configuration file and init config handler
    if os.path.exists(path):
        with open(path, 'r') as configfile:
            config.import_config(configfile.read())

    # Start log file
    logging.config.dictConfig(config.get('logs'))

    # Interactive mode
    logger = logging.getLogger(__name__)
    logger.info("ProxyPos server starting up...")
    logger.info("Listening on http://%s:%s/" % (config.get('app.host') or host,
                                                config.get('app.port') or port))
    run(app,
        host=config.get('app.host') or host,
        port=config.get('app.port') or port,
        quiet=True)

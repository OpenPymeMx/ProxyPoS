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

import yaml

from bottle import run
from app import app


def setup_logging(
    default_path='config/logging.yaml',
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    """Setup logging configuration

    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def main():
    # Set default configuration
    port = '8069'
    path = 'config/proxypos.yaml'
    # Start logg
    setup_logging()
    # Interactive mode
    logger = logging.getLogger(__name__)
    logger.info("ProxyPos server starting up...")

    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.load(f.read())
        port = config['port']

    logger.info("Listening on http://%s:%s/" % ('localhost', port))
    run(app, host='localhost', port=port, quiet=True)

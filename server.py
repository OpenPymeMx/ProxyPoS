# -*- coding: utf-8 -*-
import os
import logging.config

import yaml

from bottle import run
from main import app


def setup_logging(
    default_path='logging.yaml',
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


if __name__ == "__main__":
    # Start logg
    setup_logging()
    # Interactive mode
    logger = logging.getLogger(__name__)
    logger.info("ProxyPos server starting up...")
    logger.info("Listening on http://%s:%s/" % ('localhost', '8069'))
    run(app, host='localhost', port='8069', quiet=True)

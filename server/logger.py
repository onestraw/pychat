# -*- coding: utf-8 -*-

import logging
from const import DEBUG, LOG_FILE


logger = logging.getLogger('pychat')
formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s \
        %(message)s', '%a, %d %b %Y %H:%M:%S',)
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

if DEBUG:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

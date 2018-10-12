# -*- coding: utf-8 -*-
import logging
import os
import traceback
from datetime import datetime

from flask import request, current_app

BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
def generic_log(data):
    logger_file_name = datetime.now().strftime("%Y-%m-%d") + u'.log'
    logger_dir = os.path.join(BASEDIR, 'logs')
    if not os.path.isdir(logger_dir):
        os.makedirs(logger_dir)
    logger_dir = os.path.join(logger_dir, logger_file_name)
    handler = logging.FileHandler(logger_dir)
    if isinstance(data, Exception):
        data = traceback.format_exc()
    logging_format = logging.Formatter(
        # "%(asctime)s - %(levelname)s - %(filename)s \n- %(funcName)s - %(lineno)s - %(message)s"
        "%(asctime)s - %(levelname)s - %(filename)s \n %(message)s"
        )
    handler.setFormatter(logging_format)
    current_app.logger.addHandler(handler)
    current_app.logger.error(u'>>>>>>>>>>>>>>>>>>bug<<<<<<<<<<<<<<<<<<<')
    current_app.logger.error(data)
    current_app.logger.error(request.detail)
    current_app.logger.removeHandler(handler)

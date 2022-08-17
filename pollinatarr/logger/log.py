#!/usr/bin/python3

from __future__ import annotations

import logging
import os
import sys
import traceback
from logging.handlers import RotatingFileHandler
from typing import TYPE_CHECKING

import colorlog as colorlog

if TYPE_CHECKING:
    pass

logger: logging.Logger = logging.getLogger('Pollinatarr')

DEFAULT_LOG_DIR = "logs"


def exception_hook(exctype, value, tb):
    formatted_lines = traceback.format_exception(etype=exctype, value=value, tb=tb)
    first_line = formatted_lines[0]
    if first_line == "None":
        for line in traceback.format_stack():
            logger.error(f"{line}")
    else:
        logger.error(f"ERROR stack : {first_line}")
        for line in formatted_lines[1:]:
            logger.error(f"ERROR stack : {line}")


def get_real_log_file_path(log_file_path: str) -> str:
    if os.path.exists(os.path.dirname(log_file_path)):
        real_log_file_path = log_file_path
    elif not os.path.exists(os.path.dirname(log_file_path)) and os.path.dirname(log_file_path) != '':
        os.makedirs(DEFAULT_LOG_DIR, exist_ok=True)
        logger.warning(f"Log path {os.path.dirname(log_file_path)} is unreachable. Logs will be saved in : {os.path.join(DEFAULT_LOG_DIR, os.path.basename(log_file_path))}")
        real_log_file_path = os.path.join(DEFAULT_LOG_DIR, os.path.basename(log_file_path))
    else:
        os.makedirs(DEFAULT_LOG_DIR, exist_ok=True)
        real_log_file_path = os.path.join(DEFAULT_LOG_DIR, os.path.basename(log_file_path))
    return real_log_file_path


class StreamToLogger(object):
    def __init__(self, _logger, level):
        self.logger = _logger
        self.log_level = level
        self.linebuf = ''
    
    
    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())
    
    
    def flush(self):
        pass


def setup_logger(log_level: str, log_file: str):
    logger.setLevel(log_level)
    
    _color_formatter = colorlog.ColoredFormatter(
        '%(log_color)s [%(asctime)s] [%(levelname)s] %(message)s ', datefmt="%Y-%m-%d %H:%M:%S", log_colors={
            'DEBUG'   : 'cyan',
            'INFO'    : 'green',
            'WARNING' : 'yellow',
            'ERROR'   : 'red',
            'CRITICAL': 'red'})
    
    _formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] %(message)s ', datefmt="%Y-%m-%d %H:%M:%S")
    
    cmd_handler = logging.StreamHandler()
    cmd_handler.setLevel(log_level)
    cmd_handler.setFormatter(_color_formatter)
    logger.addHandler(cmd_handler)
    
    sys.excepthook = exception_hook
    
    log_file_path = get_real_log_file_path(log_file)
    
    file_handler = RotatingFileHandler(log_file_path, delay=True, mode="w", maxBytes=1024 * 1024 * 2, backupCount=10, encoding="utf-8")
    file_handler.setFormatter(_formatter)
    logger.addHandler(file_handler)
    
    sys.stdout = StreamToLogger(logger, logging.DEBUG)
    sys.stderr = StreamToLogger(logger, logging.ERROR)
    
    logger.debug(f"Logs are saved in {log_file_path}")

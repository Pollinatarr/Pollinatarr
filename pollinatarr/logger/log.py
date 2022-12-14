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
    from typing import Union

MAX_SUB_PART_SIZE = 24


class SubLogger(logging.Logger):
    def __init__(self, name: str, full_sub_part: str = None):
        super().__init__(name)
        self.full_sub_part = full_sub_part
    
    
    def compute_full_sub_part(self, sub_part: str):
        return f"{self.full_sub_part} [ {sub_part.ljust(MAX_SUB_PART_SIZE)} ]" if self.full_sub_part else f"[ {sub_part.ljust(MAX_SUB_PART_SIZE)} ]"
    
    
    def get_sub(self, sub_part: str) -> SubLogger:
        full_sub_part = self.compute_full_sub_part(sub_part)
        if full_sub_part in logger_cache:
            return logger_cache[full_sub_part]
        
        new_logger = SubLogger(self.name, full_sub_part)
        
        logger_cache[full_sub_part] = new_logger
        
        return new_logger
    
    
    def _log(self, level, message, args, **kwargs):
        message_format = f"{self.full_sub_part} {message}" if self.full_sub_part else message
        real_logger.log(level, message_format, *args, **kwargs)


real_logger: logging.Logger = logging.Logger("Pollinatarr")
logger: SubLogger = SubLogger("Polinatarr")

DEFAULT_LOG_DIR = "logs"

logger_cache = {}


def set_handler_on_logger(level: Union[int, str], log_file: str):
    log_header = f"[%(asctime)s] [ %(levelname)-7s ] %(message)s "
    _color_formatter = colorlog.ColoredFormatter(
        f"%(log_color)s {log_header}", datefmt="%Y-%m-%d %H:%M:%S", log_colors={
            'DEBUG'   : 'cyan',
            'INFO'    : 'green',
            'WARNING' : 'yellow',
            'ERROR'   : 'red',
            'CRITICAL': 'red'})
    
    _formatter = logging.Formatter(
        f"[%(asctime)s] {log_header}", datefmt="%Y-%m-%d %H:%M:%S")
    
    cmd_handler = logging.StreamHandler()
    cmd_handler.setLevel(level)
    cmd_handler.setFormatter(_color_formatter)
    real_logger.addHandler(cmd_handler)
    
    file_handler = RotatingFileHandler(log_file, delay=True, mode="w", maxBytes=1024 * 1024 * 2, backupCount=10, encoding="utf-8")
    file_handler.setFormatter(_formatter)
    real_logger.addHandler(file_handler)


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
    real_logger.setLevel(log_level)
    log_file_path = get_real_log_file_path(log_file)
    
    set_handler_on_logger(log_level, log_file_path)
    
    sys.excepthook = exception_hook
    
    sys.stdout = StreamToLogger(real_logger, logging.DEBUG)
    sys.stderr = StreamToLogger(real_logger, logging.ERROR)
    
    logger.debug(f"Logs are saved in {log_file_path}")

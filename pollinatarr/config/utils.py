#!/usr/bin/python3

from __future__ import annotations

from typing import TYPE_CHECKING

from pollinatarr.logger.log import logger

if TYPE_CHECKING:
    pass
DEFAULT_CONFIG_DIR_PATH = "config"
DEFAULT_CONFIG_FILE_NAME = "config.yml"
PREVENT_LOG_VARIABLE = ("password", "api_key")


class BadConfigPathException(Exception):
    pass


class MissingMandatoryPropertyException(Exception):
    pass


def get_property_from_dict(dictionary: dict, property_name: str, default_value: any = None, mandatory: bool = False, depth: int = 0, log_value: bool = True):
    reading_config_logger = logger.get_sub("CONFIG")
    _value = dictionary.get(property_name, default_value)
    if _value is None and mandatory:
        reading_config_logger.error(f"Property {property_name} is mandatory. Aborting")
        raise MissingMandatoryPropertyException()
    if log_value:
        text_for_log = ""
        for idx in range(depth):
            text_for_log += "\t\t"
        if property_name in PREVENT_LOG_VARIABLE:
            text_for_log += f"{property_name} ==> <PROTECTED_VALUE>"
        else:
            text_for_log += f"{property_name} ==> {_value}"
        reading_config_logger.info(text_for_log)
    return _value

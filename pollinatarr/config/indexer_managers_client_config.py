#!/usr/bin/python3

from __future__ import annotations

from typing import TYPE_CHECKING

from pollinatarr.config.utils import get_property_from_dict
from pollinatarr.logger.log import logger

if TYPE_CHECKING:
    pass


class UnknownIndexerManager(Exception):
    def __init__(self, indexer_manager_name):
        self.indexer_manager_name = indexer_manager_name


class IndexerManagerClientConfig(object):
    def __init__(self):
        self.host = None
        self.api_key = None
        pass
    
    
    @staticmethod
    def from_dict(client_name: str, _dict: dict):
        logger.info(f"\t\tLoading indexer manager client {client_name} configuration")


class ProwlarrClientConfig(IndexerManagerClientConfig):
    def __init__(self):
        super().__init__()
    
    
    @staticmethod
    def from_dict(client_name: str, _dict: dict) -> ProwlarrClientConfig:
        IndexerManagerClientConfig.from_dict(client_name, _dict)
        config = ProwlarrClientConfig()
        config.host = get_property_from_dict(_dict, "host", mandatory=True, depth=2)
        config.api_key = get_property_from_dict(_dict, "api_key", mandatory=True, depth=2)
        return config

#!/usr/bin/python3

from __future__ import annotations

from typing import TYPE_CHECKING

from uncross_seed.config.indexer_managers_client_config import IndexerManagerClientConfig

if TYPE_CHECKING:
    pass


class AbstractIndexerManager(object):
    def __init__(self, config: IndexerManagerClientConfig):
        self.host = config.host
        self.api_key = config.api_key
    
    
    def search_by_name(self, _name: str, **opts):
        raise NotImplementedError

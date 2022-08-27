#!/usr/bin/python3

from __future__ import annotations

from typing import TYPE_CHECKING

from pollinatarr.indexer_manager.prowlarr import ProwlarrClient
from pollinatarr.logger.log import logger

if TYPE_CHECKING:
    from pollinatarr.config.config import Config
    from pollinatarr.indexer_manager.abstract_indexer_manager import AbstractIndexerManager

INDEXER_MANAGER_CLIENT_MAPPING = {
    "prowlarr": ProwlarrClient
}


def create_indexer_manager_clients_from_config(config: Config) -> dict[str, AbstractIndexerManager]:
    indexer_manager_clients = {}
    index_manager_factory_logger = logger.get_sub("INDEX MANAGER FACTORY")
    index_manager_factory_logger.info("Creating indexer manager clients")
    for _indexer_manager_name, _indexer_manager_config in config.indexer_manager_clients.items():
        index_manager_factory_logger.info(f"Creating {_indexer_manager_name} client")
        indexer_manager_clients[_indexer_manager_name] = INDEXER_MANAGER_CLIENT_MAPPING[_indexer_manager_name](_indexer_manager_config)
    index_manager_factory_logger.info("Indexer manager clients created")
    return indexer_manager_clients

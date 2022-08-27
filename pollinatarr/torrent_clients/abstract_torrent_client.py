#!/usr/bin/python3

from __future__ import annotations

from abc import ABCMeta
from typing import TYPE_CHECKING

from pollinatarr.logger.log import logger
from pollinatarr.torrents.torrent_container import TorrentContainer

if TYPE_CHECKING:
    from pollinatarr.config.config import Config
    from pollinatarr.config.torrent_clients_config import TorrentClientConfig


class FailedToConnect(Exception):
    pass


class AbstractTorrentClient(object, metaclass=ABCMeta):
    def __init__(self, config: TorrentClientConfig, name: str):
        self.name = name
        self.config = config
        self.logger = logger.get_sub("TORRENT CLIENT").get_sub(name)
    
    
    def get_torrents_using_config(self, config: Config) -> TorrentContainer:
        torrents = TorrentContainer()
        for _tracker_name, _tracker_config in config.trackers.items():
            categories = _tracker_config.categories or config.categories
            for category in categories:
                self.logger.info(f"Searching torrents that match {category} category and {_tracker_name} tracker")
                _torrents = self.get_torrents_from_tracker(_tracker_name, category)
                self.logger.info(f"Found {len(_torrents)} torrents")
                torrents.merge(_torrents)
        return torrents
    
    
    def get_torrents_from_tracker(self, tracker_name: str, category: str) -> TorrentContainer:
        raise NotImplementedError

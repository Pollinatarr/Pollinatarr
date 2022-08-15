#!/usr/bin/python3

from __future__ import annotations

from abc import ABCMeta
from typing import TYPE_CHECKING

from uncross_seed.logger.log import logger

if TYPE_CHECKING:
    from uncross_seed.config.config import Config
    from uncross_seed.config.torrent_clients_config import TorrentClientConfig


class FailedToConnect(Exception):
    pass


class AbstractTorrentClient(object, metaclass=ABCMeta):
    def __init__(self, config: TorrentClientConfig):
        pass
    
    def get_torrents_using_config(self, config: Config) -> dict:
        torrents_per_category = {_category_name: {} for _category_name in config.categories}
        for _tracker_name, _tracker_config in config.trackers.items():
            categories = _tracker_config.categories or config.categories
            for category in categories:
                logger.info(f"Searching torrents that match {category} category and {_tracker_name} tracker")
                _torrents = self.get_torrents_name_from_tracker(_tracker_name, category)
                logger.info(f"Found {len(_torrents)} torrents")
                for _torrent in _torrents:
                    if _torrent in torrents_per_category[category]:
                        torrents_per_category[category][_torrent].append(_tracker_name)
                    else:
                        torrents_per_category[category][_torrent] = [_tracker_name]
        return torrents_per_category

    
    def get_torrents_from_tracker(self, tracker_name: str, category: str) -> list:
        raise NotImplementedError
        
    def get_torrents_name_from_tracker(self, tracker_name: str, category: str) -> list:
        raise NotImplementedError

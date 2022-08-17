#!/usr/bin/python3

from __future__ import annotations

from typing import TYPE_CHECKING

from pollinatarr.config.utils import get_property_from_dict
from pollinatarr.logger.log import logger

if TYPE_CHECKING:
    pass


class UnknownTorrentClient(Exception):
    def __init__(self, torrent_client):
        self.torrent_client = torrent_client


class TorrentClientConfig(object):
    def __init__(self):
        pass
    
    
    @staticmethod
    def from_dict(client_name: str, _dict: dict):
        logger.info(f"\t\tLoading torrent client {client_name} configuration")


class qBittorrentClientConfig(TorrentClientConfig):
    def __init__(self):
        super().__init__()
        self.host = None
        self.username = None
        self.password = None
    
    
    @staticmethod
    def from_dict(client_name: str, _dict: dict) -> qBittorrentClientConfig:
        TorrentClientConfig.from_dict(client_name, _dict)
        config = qBittorrentClientConfig()
        config.host = get_property_from_dict(_dict, "host", mandatory=True, depth=2)
        config.username = get_property_from_dict(_dict, "username", mandatory=True, depth=2)
        config.password = get_property_from_dict(_dict, "password", mandatory=True, depth=2)
        return config

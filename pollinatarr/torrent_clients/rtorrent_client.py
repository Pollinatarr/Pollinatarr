#!/usr/bin/python3

from __future__ import annotations

from typing import TYPE_CHECKING
from urllib.parse import urlparse

from rtorrent import RTorrent, MIN_RTORRENT_VERSION

from pollinatarr.torrent_clients.abstract_torrent_client import AbstractTorrentClient, FailedToConnect
from pollinatarr.torrents.torrent import Torrent
from pollinatarr.torrents.torrent_container import TorrentContainer

if TYPE_CHECKING:
    from typing import Optional
    from pollinatarr.config.torrent_clients_config import rTorrentClientConfig
    from qbittorrentapi import TorrentDictionary


class rTorrentClient(AbstractTorrentClient):
    def __init__(self, config: rTorrentClientConfig):
        self.config: Optional[rTorrentClientConfig] = None
        super().__init__(config, name="rTorrent")
        self.client: Optional[RTorrent] = None
        self.do_connect()
    
    
    @staticmethod
    def _construct_url_from_config(config: rTorrentClientConfig) -> str:
        if config.auth:
            split_url = config.host.split("://")
            protocol = split_url[0]
            url_end = split_url[1]
            return f"{protocol}://{config.username}:{config.password}@{url_end}"
        return config.host
    
    
    def do_connect(self):
        try:
            self.client = RTorrent(self._construct_url_from_config(self.config))
            self.logger.debug(f'Version: {self.client.get_client_version()}')
            self.logger.debug(f'Supported version: Min {MIN_RTORRENT_VERSION}')
        except Exception as e:
            e = f"Error while connecting to rTorrent: Unable to connect to the client for unexpected exception : {e}"
            raise FailedToConnect(e)
    
    
    @staticmethod
    def create_torrent_container_from_torrent_dictionary_list(raw_torrents_list: list[TorrentDictionary]) -> TorrentContainer:
        torrents = TorrentContainer()
        for raw_torrent in raw_torrents_list:
            _torrent = Torrent(raw_torrent.name, raw_torrent.category)
            for tracker in raw_torrent.trackers:
                _torrent.add_tracker(urlparse(tracker.url).hostname)
            torrents.add_torrent(_torrent)
        return torrents
    
    
    def get_torrents_from_tracker(self, tracker_name: str, category: str) -> TorrentContainer:
        _unsorted_torrents = self.client.get_torrents()
        _torrents = [_torrent for _torrent in self.client.get_torrents() if next((tracker for tracker in _torrent.get_trackers() if tracker_name in tracker.url), None) and _torrent.category == category]
        return self.create_torrent_container_from_torrent_dictionary_list(_torrents)

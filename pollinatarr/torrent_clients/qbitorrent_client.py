#!/usr/bin/python3

from __future__ import annotations

from typing import TYPE_CHECKING

import qbittorrentapi
from qbittorrentapi import Client, LoginFailed, APIConnectionError

from pollinatarr.config.torrent_clients_config import qBittorrentClientConfig
from pollinatarr.logger.log import logger
from pollinatarr.torrent_clients.abstract_torrent_client import AbstractTorrentClient, FailedToConnect
from pollinatarr.torrents.torrent import Torrent
from pollinatarr.torrents.torrent_container import TorrentContainer

if TYPE_CHECKING:
    from qbittorrentapi import TorrentDictionary


class qBittorrentClient(AbstractTorrentClient):
    def __init__(self, config: qBittorrentClientConfig):
        super().__init__(config, name="qBittorrent")
        self.client = Client(host=config.host, username=config.username, password=config.password, VERIFY_WEBUI_CERTIFICATE=False)
        self.do_connect()
    
    
    def do_connect(self):
        try:
            self.client.auth_log_in()
            self.logger.debug(f'Version: {self.client.app.version}')
            self.logger.debug(f'Web API version: {self.client.app.web_api_version}')
            self.logger.debug(f'Supported version: {qbittorrentapi.Version.supported_app_versions()}')
        except LoginFailed:
            e = "Error while connecting to qBittorrent: Bad username/password."
            raise FailedToConnect(e)
        except APIConnectionError:
            e = "Error while connecting to qBittorrent: Unable to connect to the client."
            raise FailedToConnect(e)
        except Exception as e:
            e = f"Error while connecting to qBittorrent: Unable to connect to the client for unexpected exception : {e}"
            raise FailedToConnect(e)
    
    
    def do_disconnect(self):
        self.client.auth_log_out()
        self.logger.debug(f'Disconnected from client')
    
    
    @staticmethod
    def create_torrent_container_from_torrent_dictionary_list(raw_torrents_list: list[TorrentDictionary]) -> TorrentContainer:
        torrents = TorrentContainer()
        for raw_torrent in raw_torrents_list:
            _torrent = Torrent(raw_torrent.name, raw_torrent.category)
            for tracker in raw_torrent.trackers:
                _torrent.add_tracker(tracker)
            torrents.add_torrent(_torrent)
        return torrents
    
    
    def get_torrents_from_tracker(self, tracker_name: str, category: str) -> TorrentContainer:
        _torrents = [_torrent for _torrent in self.client.torrents.info(category=category, sort="added_on").data if next((tracker for tracker in _torrent.trackers.data if tracker_name in tracker.url), None)]
        return self.create_torrent_container_from_torrent_dictionary_list(_torrents)

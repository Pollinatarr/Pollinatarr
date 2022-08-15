#!/usr/bin/python3

from __future__ import annotations

from typing import TYPE_CHECKING

import qbittorrentapi
from qbittorrentapi import Client, LoginFailed, APIConnectionError

from uncross_seed.config.torrent_clients_config import qBittorrentClientConfig
from uncross_seed.logger.log import logger
from uncross_seed.torrent_clients.abstract_torrent_client import AbstractTorrentClient, FailedToConnect

if TYPE_CHECKING:
    pass


class qBittorrentClient(AbstractTorrentClient):
    def __init__(self, config: qBittorrentClientConfig):
        super().__init__(config)
        self.client = Client(host=config.host, username=config.username, password=config.password, VERIFY_WEBUI_CERTIFICATE=False)
        self.do_connect()
    
    def do_connect(self):
        try:
            self.client.auth_log_in()
            logger.debug(f'qBittorrent: {self.client.app.version}')
            logger.debug(f'qBittorrent Web API: {self.client.app.web_api_version}')
            logger.debug(f'Supported version: {qbittorrentapi.Version.supported_app_versions()}')
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
        logger.debug(f'Disconnected from qBittorrent')
    
    
    def get_torrents_name_from_tracker(self, tracker_name: str, category: str) -> list:
        _torrents = [_torrent.name for _torrent in self.client.torrents.info(category=category, sort="added_on").data if next((tracker for tracker in _torrent.trackers.data if tracker_name in tracker.url), None)]
        return _torrents
    
    
    def get_torrents_from_tracker(self, tracker_name: str, category: str) -> list:
        _torrents = [_torrent for _torrent in self.client.torrents.info(category=category, sort="added_on").data if next((tracker for tracker in _torrent.trackers.data if tracker_name in tracker.url), None)]
        return _torrents
        

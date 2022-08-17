#!/usr/bin/python3

from __future__ import annotations

from typing import TYPE_CHECKING

from pollinatarr.logger.log import logger
from pollinatarr.torrent_clients.qbitorrent_client import qBittorrentClient

if TYPE_CHECKING:
    from pollinatarr.config.config import Config
    from pollinatarr.torrent_clients.abstract_torrent_client import AbstractTorrentClient

TORRENT_CLIENT_MAPPING = {
    "qbittorrent": qBittorrentClient
}


def create_torrents_client_from_config(config: Config) -> list[AbstractTorrentClient]:
    torrent_clients = []
    logger.info("Creating torrent clients")
    for _torrent_client_name, _torrent_client_config in config.torrent_clients.items():
        logger.info(f"Creating {_torrent_client_name} client")
        torrent_clients.append(TORRENT_CLIENT_MAPPING[_torrent_client_name](_torrent_client_config))
    logger.info("Torrent clients created")
    return torrent_clients

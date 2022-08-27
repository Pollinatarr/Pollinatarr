#!/usr/bin/python3

from __future__ import annotations

from typing import TYPE_CHECKING

from prettytable import PrettyTable

from pollinatarr.logger.log import logger

if TYPE_CHECKING:
    from pollinatarr.torrents.torrent_container import TorrentContainer


def display_torrents_per_trackers_in_beautiful_table(_torrents: TorrentContainer):
    table = PrettyTable()
    table.field_names = ["Torrent name", "Trackers without the torrent"]
    for torrent in _torrents.torrents:
        table.add_row([torrent.torrent_name, ", ".join(torrent.trackers)])
    
    logger.info(f"\n{table.get_string()}")

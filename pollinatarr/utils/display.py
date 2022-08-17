#!/usr/bin/python3

from __future__ import annotations

from typing import TYPE_CHECKING

from prettytable import PrettyTable

from pollinatarr.logger.log import logger

if TYPE_CHECKING:
    pass


def display_torrents_per_trackers_in_beautiful_table(_torrents_per_trackers: dict):
    table = PrettyTable()
    table.field_names = ["Torrent name", "Trackers without the torrent"]
    for _, _cat in _torrents_per_trackers.items():
        for torrent_name, trackers in _cat.items():
            table.add_row([torrent_name, ", ".join(trackers)])
    
    logger.info(f"\n{table.get_string()}")

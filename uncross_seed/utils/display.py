#!/usr/bin/python3

from __future__ import annotations

from typing import TYPE_CHECKING

from prettytable import PrettyTable

from uncross_seed.logger.log import logger

if TYPE_CHECKING:
    pass


def display_uncross_seed_torrents_in_beautiful_table(_uncross_seed_torrents: dict):
    table = PrettyTable()
    table.field_names = ["Torrent name", "Trackers without the torrent"]
    for _, _cat in _uncross_seed_torrents.items():
        for torrent_name, trackers in _cat.items():
            table.add_row([torrent_name, ", ".join(trackers)])
    
    logger.info(f"\n{table.get_string()}")

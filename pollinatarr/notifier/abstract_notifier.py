#!/usr/bin/python3

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pollinatarr.config.notifier_config import NotifierConfig


class AbstractNotifier:
    def __init__(self, config: NotifierConfig):
        self.config = config
    
    
    def run_start(self, start_time, run_mode):
        raise NotImplementedError
    
    
    def run_end(self, start_time, end_time, result, only_display, searching_on_clients_time=None, searching_on_indexers_time=None):
        raise NotImplementedError
    
    
    @staticmethod
    def _format_result(result):
        dict_result = {}
        for torrent in result:
            for tracker in torrent.get("trackers", []):
                if tracker in dict_result:
                    dict_result[tracker].append(torrent.get("torrent_name"))
                else:
                    dict_result[tracker] = [torrent.get("torrent_name")]
        return dict_result

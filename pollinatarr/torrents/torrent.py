#!/usr/bin/python3

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class Torrent(object):
    def __init__(self, torrent_name: str, category_name: str):
        self.torrent_name = torrent_name
        self.category = category_name
        self.trackers = []
    
    
    def add_tracker(self, tracker_name: str):
        self.trackers.append(tracker_name)
    
    
    def merge(self, another: Torrent):
        for tracker in another.trackers:
            self.trackers.append(tracker)
    
    
    def to_dict(self):
        return {"torrent_name": self.torrent_name,
                "category"    : self.category,
                "trackers"    : self.trackers}
    
    
    @staticmethod
    def from_dict(_dict) -> Torrent:
        torrent = Torrent(_dict.get("torrent_name"), _dict.get("category"))
        torrent.trackers = set(_dict.get("trackers"))
        return torrent

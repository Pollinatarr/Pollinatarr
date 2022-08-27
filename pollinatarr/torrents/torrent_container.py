#!/usr/bin/python3

from __future__ import annotations

from typing import TYPE_CHECKING

from pollinatarr.torrents.torrent import Torrent

if TYPE_CHECKING:
    pass


class TorrentContainer(object):
    def __init__(self):
        self.torrents: list[Torrent] = []
    
    
    def callback_on_remove(self, torrent: Torrent):
        pass
    
    
    def add_torrent(self, torrent: Torrent):
        if torrent is None:
            pass
        self.torrents.append(torrent)
    
    
    def remove_torrent(self, torrent: Torrent):
        self.torrents.remove(torrent)
    
    
    def find_torrent_by_name(self, torrent_name: str) -> Torrent:
        try:
            return next((torrent for torrent in self.torrents if torrent.torrent_name == torrent_name), None)
        except AttributeError:
            pass
    
    
    def find_torrents_with_category(self, category_name: str) -> list:
        return [torrent for torrent in self.torrents if torrent.category == category_name]
    
    
    def find_torrents_with_tracker(self, tracker_name: str) -> list:
        return [torrent for torrent in self.torrents if tracker_name in torrent.trackers]
    
    
    def merge(self, another: TorrentContainer):
        for torrent in another.torrents:
            my_torrent = self.find_torrent_by_name(torrent.torrent_name)
            if my_torrent:
                my_torrent.merge(torrent)
            else:
                self.torrents.append(torrent)
    
    
    def __len__(self):
        return len(self.torrents)
    
    
    def to_dict(self):
        return [torrent.to_dict() for torrent in self.torrents]
    
    
    @staticmethod
    def from_dict(_dict):
        torrent_container = TorrentContainer()
        for _raw_torrent in _dict:
            torrent_container.add_torrent(Torrent.from_dict(_raw_torrent))
        return torrent_container

#!/usr/bin/python3

from __future__ import annotations

import json
import os
import time
from typing import TYPE_CHECKING

from pollinatarr.config.config import Config
from pollinatarr.indexer_manager.abstract_indexer_manager import AbstractIndexerManager
from pollinatarr.indexer_manager.indexer_manager_factory import create_indexer_manager_clients_from_config
from pollinatarr.logger.log import setup_logger, logger
from pollinatarr.torrent_clients.abstract_torrent_client import AbstractTorrentClient
from pollinatarr.torrent_clients.torrent_client_factory import create_torrents_client_from_config
from pollinatarr.utils.display import display_torrents_per_trackers_in_beautiful_table

if TYPE_CHECKING:
    pass

import argparse
import sys

DEFAULT_RESULT_DIR_PATH = "result"
DEFAULT_RESULT_FILE_NAME = "result.json"


def write_file_result(torrents: dict[str, dict[str, list[str]]], result_path: str):
    logger.info(f"Writing result on {result_path}")
    with open(result_path, "w+") as f:
        f.write(json.dumps(torrents))
    logger.info(f"Result correctly saved")


def search_torrents_with_indexer_manager(torrents: dict[str, dict[str, list[str]]], config: Config, indexer_manager_clients: dict[str, AbstractIndexerManager]) -> dict[str, dict[str, list[str]]]:
    torrents_per_trackers = {}
    torrents_nb = 0
    for _cat_name, _cat in torrents.items():
        logger.info(f"Searching torrents in category {_cat_name}")
        torrents_per_trackers[_cat_name] = {}
        _trackers_with_this_cat = [(tracker_name, tracker) for tracker_name, tracker in config.trackers.items() if _cat_name in tracker.categories]
        for torrent_name, trackers in _cat.items():
            torrent_name = torrent_name.strip(".mkv")
            tracker_to_search_on = [tracker_tuple for tracker_tuple in _trackers_with_this_cat if tracker_tuple[0] not in trackers and not tracker_tuple[1].ignore_searching]
            for tracker in tracker_to_search_on:
                tracker_name = tracker[0]
                for indexer_manager_wanted, _opts in tracker[1].indexers.items():
                    logger.debug(f"Searching {torrent_name} for tracker {tracker_name} with indexer manager {indexer_manager_wanted}")
                    torrent_found = bool(next((_t for _t in indexer_manager_clients[indexer_manager_wanted].search_by_name(torrent_name, **_opts) if _t.get("title", "") == torrent_name), None))
                    if torrent_found:
                        logger.debug(f"{torrent_name} found on tracker {tracker_name} with indexer manager {indexer_manager_wanted}")
                        break
                    else:
                        logger.debug(f"{torrent_name} not found on tracker {tracker_name} with indexer manager {indexer_manager_wanted}")
                else:
                    if torrent_name in torrents_per_trackers[_cat_name]:
                        torrents_per_trackers[_cat_name][torrent_name].append(tracker_name)
                    else:
                        torrents_per_trackers[_cat_name][torrent_name] = [tracker_name]
        nb_per_category = len(torrents_per_trackers[_cat_name])
        torrents_nb += nb_per_category
        logger.info(f"All torrents from category {_cat_name} have been searched")
        logger.info(f"There are {nb_per_category} torrents in the {_cat_name} category that you can upload on other trackers")
    logger.info(f"There are {torrents_nb} torrents you can upload on other trackers")
    return torrents_per_trackers


def remove_torrents_already_cross_seeded(torrents: dict[str, dict[str, list[str]]], config: Config):
    for _cat_name, _cat in torrents.items():
        torrents_nb = len(_cat)
        _torrents_to_remove = []
        _trackers_with_this_cat = [tracker_name for tracker_name, tracker in config.trackers.items() if _cat_name in tracker.categories]
        for torrent_name, trackers in _cat.items():
            if trackers == _trackers_with_this_cat:
                _torrents_to_remove.append(torrent_name)
        
        for torrent_to_remove in _torrents_to_remove:
            logger.debug(f"The torrent {torrent_to_remove} is already cross-seeded, removing it")
            _cat.pop(torrent_to_remove)
        logger.info(f"{torrents_nb - len(_cat)} torrents are already cross-seeded in {_cat_name}")
    nb_of_torrents = sum([len(torrents_per_cat) for _cat_name, torrents_per_cat in torrents.items()])
    logger.info(f"{nb_of_torrents} torrents remaining")


def find_all_torrents(config: Config, torrent_clients: list[AbstractTorrentClient]):
    torrents: dict[str, dict[str, list[str]]] = {}
    for torrent_client in torrent_clients:
        torrents = torrents | torrent_client.get_torrents_using_config(config)
    nb_of_torrents = sum([len(torrents_per_cat) for _cat_name, torrents_per_cat in torrents.items()])
    logger.info(f"Found {nb_of_torrents} torrents in your clients")
    return torrents


def get_result_file_path(result_path: str) -> str:
    if result_path and os.path.dirname(result_path) and os.path.exists(os.path.dirname(result_path)):
        real_config_path = os.path.abspath(result_path)
    elif result_path and os.path.exists(DEFAULT_RESULT_DIR_PATH):
        real_config_path = os.path.abspath(os.path.join(DEFAULT_RESULT_DIR_PATH, result_path))
    else:
        logger.error(f"Error: result unreachable at {os.path.abspath(result_path)}")
        sys.exit(1)
    return real_config_path


if __name__ == '__main__':
    if sys.version_info[0] != 3 or sys.version_info[1] < 10:
        print("Version Error: Version: %s.%s.%s incompatible please use Python 3.10+" % (sys.version_info[0], sys.version_info[1], sys.version_info[2]))
        sys.exit(0)
    
    parser = argparse.ArgumentParser('uncross seed', description='Find the torrents you can share with you trackers')
    parser.add_argument('-c', '--config-file', dest='config_file', action='store', default='config.yml', type=str,
                        help='Choose config file path')
    parser.add_argument('-lf', '--log-file', dest='log_file', action='store', default='activity.log', type=str, help='Change you log file name', )
    parser.add_argument('-ll', '--log-level', dest='log_level', action="store", default='INFO', type=str, help='Change your log level.')
    parser.add_argument('-wt', '--wait-time', dest='wait_time', action="store", default=2, type=int, help='Will set the waiting time between two request to Prowlarr')
    parser.add_argument('-rf', '--result-file', dest='result_file', action="store", default='result.json', type=str, help='Change you result file name')
    parser.add_argument('-od', '--only-display', dest='only_display', action="store_true", help='Only display in a great table the result file (defined with -rf)')
    args = parser.parse_args()
    
    setup_logger(args.log_level, args.log_file)
    
    _result_path = get_result_file_path(args.result_file)
    
    if not args.only_display:
        _config = Config.load_config(args.config_file)
        
        _torrent_clients = create_torrents_client_from_config(_config)
        _indexer_manager_clients = create_indexer_manager_clients_from_config(_config)
        
        start_time = time.time()
        _torrents = find_all_torrents(_config, _torrent_clients)
        logger.info(f"Finding all torrents took {time.time() - start_time} seconds")
        
        start_time = time.time()
        remove_torrents_already_cross_seeded(_torrents, _config)
        logger.info(f"Filtering torrents took {time.time() - start_time} seconds")
    
        start_time = time.time()
        _torrents_to_pollinate = search_torrents_with_indexer_manager(_torrents, _config, _indexer_manager_clients)
        logger.info(f"Searching torrents through indexer manager took {time.time() - start_time} seconds")
    
        write_file_result(_torrents_to_pollinate, _result_path)
    else:
        with open(_result_path, "r") as f:
            _torrents_to_pollinate = json.load(f)
            
    display_torrents_per_trackers_in_beautiful_table(_torrents_to_pollinate)

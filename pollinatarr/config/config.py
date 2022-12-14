#!/usr/bin/python3

from __future__ import annotations

import os
import sys
from typing import TYPE_CHECKING

import yaml

from pollinatarr.config.indexer_managers_client_config import IndexerManagerClientConfig, ProwlarrClientConfig, UnknownIndexerManager
from pollinatarr.config.notifier_config import NotifierConfig, WebhookNotifierConfig, DiscordNotifierConfig, UnknownNotifier
from pollinatarr.config.torrent_clients_config import TorrentClientConfig, qBittorrentClientConfig, UnknownTorrentClient, rTorrentClientConfig
from pollinatarr.config.utils import DEFAULT_CONFIG_DIR_PATH, DEFAULT_CONFIG_FILE_NAME, BadConfigPathException, get_property_from_dict
from pollinatarr.logger.log import logger

if TYPE_CHECKING:
    from typing import Optional

NOTIFIER_CONFIG_MAP = {
    "discord": DiscordNotifierConfig,
    "webhook": WebhookNotifierConfig
}

TORRENT_CLIENT_CONFIG_MAP = {
    "qbittorrent": qBittorrentClientConfig,
    "rTorrent"   : rTorrentClientConfig
}

INDEXER_MANAGER_CONFIG_MAP = {
    "prowlarr": ProwlarrClientConfig
}


class TrackerConfig(object):
    def __init__(self):
        self.indexers: dict[str, dict] = {}
        self.categories: list[str] = []
        self.ignore_searching: bool = False
    
    
    @staticmethod
    def from_dict(_tracker_name: str, _dict: dict) -> TrackerConfig:
        reading_config_logger = logger.get_sub("CONFIG")
        reading_config_logger.info(f"\t\tLoading tracker {_tracker_name} configuration")
        config = TrackerConfig()
        config.indexers = get_property_from_dict(_dict, "indexer_managers", mandatory=True, depth=2)
        config.categories = get_property_from_dict(_dict, "categories", default_value=[], mandatory=False, depth=2)
        config.ignore_searching = get_property_from_dict(_dict, "ignore_searching", mandatory=False, depth=2, default_value=False)
        return config


class Config(object):
    def __init__(self):
        self.config_path: Optional[str] = None
        self.torrent_clients: dict[str, TorrentClientConfig] = {}
        self.indexer_manager_clients: dict[str, IndexerManagerClientConfig] = {}
        self.categories: list[str] = []
        self.trackers: dict[str, TrackerConfig] = {}
        self.notifiers: dict[str, Optional[NotifierConfig]] = {"discord": None, "webhook": None}
    
    
    @staticmethod
    def from_dict(_dict: dict, config_path: str) -> Config:
        reading_config_logger = logger.get_sub("CONFIG")
        reading_config_logger.info("Loading base configuration")
        config = Config()
        config.config_path = config_path
        config.categories = get_property_from_dict(_dict, "categories", mandatory=True, depth=1)
        
        for _notifier_type, _notifier_dict in get_property_from_dict(_dict, "notifiers", mandatory=True, log_value=False).items():
            _notifier_config = NOTIFIER_CONFIG_MAP.get(_notifier_type, None)
            if _notifier_config:
                config.notifiers[_notifier_type] = _notifier_config.from_dict(_notifier_dict, )
            else:
                raise UnknownNotifier(_notifier_type)
        
        for _torrent_client_name, _torrent_client_dict in get_property_from_dict(_dict, "torrent_clients", mandatory=True, log_value=False).items():
            _torrent_client_config = TORRENT_CLIENT_CONFIG_MAP.get(_torrent_client_name, None)
            if _torrent_client_config:
                config.torrent_clients[_torrent_client_name] = _torrent_client_config.from_dict(_torrent_client_name, _torrent_client_dict)
            else:
                raise UnknownTorrentClient(_torrent_client_name)
        
        for _indexer_manager_client_name, _indexer_manager_client_dict in get_property_from_dict(_dict, "indexer_managers", mandatory=True, log_value=False).items():
            _indexer_manager_config = INDEXER_MANAGER_CONFIG_MAP.get(_indexer_manager_client_name, None)
            if _indexer_manager_config:
                config.indexer_manager_clients[_indexer_manager_client_name] = _indexer_manager_config.from_dict(_indexer_manager_client_name, _indexer_manager_client_dict)
            else:
                raise UnknownIndexerManager(_indexer_manager_client_name)
        
        for _tracker_name, _tracker_dict in get_property_from_dict(_dict, "trackers", mandatory=True, log_value=False).items():
            config.trackers[_tracker_name] = TrackerConfig.from_dict(_tracker_name, _tracker_dict)
        return config
    
    
    @staticmethod
    def load_config(config_path: str) -> Config:
        reading_config_logger = logger.get_sub("CONFIG")
        reading_config_logger.info("Loading configuration")
        if config_path and os.path.exists(config_path):
            real_config_path = os.path.abspath(config_path)
        elif config_path and os.path.exists(os.path.join(DEFAULT_CONFIG_DIR_PATH, config_path)):
            real_config_path = os.path.abspath(os.path.join(DEFAULT_CONFIG_DIR_PATH, config_path))
        elif config_path and not os.path.exists(config_path):
            raise BadConfigPathException(f"Config Error: config not found at {os.path.abspath(config_path)}")
        elif os.path.exists(os.path.join(DEFAULT_CONFIG_DIR_PATH, DEFAULT_CONFIG_FILE_NAME)):
            real_config_path = os.path.abspath(os.path.join(DEFAULT_CONFIG_DIR_PATH, DEFAULT_CONFIG_FILE_NAME))
        else:
            raise BadConfigPathException(f"Config Error: config not found at {os.path.abspath(DEFAULT_CONFIG_DIR_PATH)}")
        reading_config_logger.info(f"Loading config from {real_config_path}")
        
        with open(real_config_path, "r") as f:
            config_dict = yaml.safe_load(f)
        
        try:
            _config = Config.from_dict(config_dict, real_config_path)
        except UnknownTorrentClient as e:
            reading_config_logger.error(f"The torrent client {e.torrent_client} is not supported. Aborting")
            sys.exit(1)
        except UnknownIndexerManager as e:
            reading_config_logger.error(f"The indexer manager {e.indexer_manager_name} is not supported. Aborting")
            sys.exit(1)
        reading_config_logger.info("Configuration correctly loaded")
        return _config

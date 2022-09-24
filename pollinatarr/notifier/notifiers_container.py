#!/usr/bin/python3

from __future__ import annotations

from typing import TYPE_CHECKING

from pollinatarr.logger.log import logger
from pollinatarr.notifier.discord_notifier import DiscordNotifier
from pollinatarr.notifier.webhook_notifier import WebhookNotifier

if TYPE_CHECKING:
    from pollinatarr.config.config import Config
    from pollinatarr.notifier.abstract_notifier import AbstractNotifier

TORRENT_CLIENT_MAPPING = {
    "discord": DiscordNotifier,
    "webhook": WebhookNotifier
}


class NotifiersContainer:
    def __init__(self):
        self.notifiers: list[AbstractNotifier] = []
    
    
    def create_notifiers_from_config(self, config: Config):
        notifier_factory_logger = logger.get_sub("NOTIFIER FACTORY")
        notifier_factory_logger.info("Creating notifiers")
        for _notifier_name, _notifier_config in config.notifiers.items():
            notifier_factory_logger.info(f"Creating {_notifier_name} client")
            self.notifiers.append(TORRENT_CLIENT_MAPPING[_notifier_name](_notifier_config))
        notifier_factory_logger.info("Notifiers created")
    
    
    def run_start(self, start_time, run_mode):
        for notifier in self.notifiers:
            notifier.run_start(start_time, run_mode)
    
    
    def run_end(self, start_time, end_time, result, only_display, searching_on_clients_time=None, searching_on_indexers_time=None):
        for notifier in self.notifiers:
            notifier.run_end(start_time, end_time, result, only_display, searching_on_clients_time, searching_on_indexers_time)

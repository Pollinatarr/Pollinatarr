#!/usr/bin/python3

from __future__ import annotations

from typing import TYPE_CHECKING

from pollinatarr.config.utils import get_property_from_dict

if TYPE_CHECKING:
    pass


class UnknownNotifier(Exception):
    def __init__(self, notifier):
        self.notifier = notifier


class NotifierConfig(object):
    def __init__(self):
        self.run_start = None
        self.run_end = None
    
    
    def set_notification_type_from_dict(self, _dict):
        self.run_start = get_property_from_dict(_dict, "run_start", mandatory=False, depth=2)
        self.run_end = get_property_from_dict(_dict, "run_end", mandatory=False, depth=2)


class DiscordNotifierConfig(NotifierConfig):
    def __init__(self):
        super().__init__()
    
    
    @staticmethod
    def from_dict(_dict: dict) -> DiscordNotifierConfig:
        config = DiscordNotifierConfig()
        config.set_notification_type_from_dict(_dict)
        return config


class WebhookNotifierConfig(NotifierConfig):
    def __init__(self):
        super().__init__()
    
    
    @staticmethod
    def from_dict(_dict: dict) -> WebhookNotifierConfig:
        config = WebhookNotifierConfig()
        config.set_notification_type_from_dict(_dict)
        return config

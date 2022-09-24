#!/usr/bin/python3

from __future__ import annotations

from datetime import datetime
from json import JSONDecodeError
from typing import TYPE_CHECKING

import requests

from pollinatarr.notifier.abstract_notifier import AbstractNotifier

if TYPE_CHECKING:
    from pollinatarr.config.notifier_config import WebhookNotifierConfig


class WebhookFailed(Exception):
    pass


class WebhookNotifier(AbstractNotifier):
    def __init__(self, config: WebhookNotifierConfig):
        super().__init__(config)
        self.session = requests.Session()
    
    
    def do_request(self, webhook: str, json: dict):
        response = self.session.post(webhook, json=json)
        if response:
            try:
                response_json = response.json()
                if response.status_code >= 400 or ("result" in response_json and response_json["result"] == "error"):
                    raise WebhookFailed(f"({response.status_code} [{response.reason}]) {response_json}")
            except JSONDecodeError:
                if response.status_code >= 400:
                    raise WebhookFailed(f"({response.status_code} [{response.reason}])")
    
    
    def run_start(self, start_time, run_mode):
        if self.config.run_start:
            start_time = datetime.fromtimestamp(start_time)
            self.do_request(self.config.run_start, {
                "function"  : "run_start",
                "body"      : "Starting run",
                "title"     : None,
                "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
                "run_mode"  : run_mode})
    
    
    def run_end(self, start_time, end_time, result, only_display, searching_on_clients_time=None, searching_on_indexers_time=None):
        if self.config.run_end:
            start_time = datetime.fromtimestamp(start_time)
            end_time = datetime.fromtimestamp(end_time)
            json_result = {"function"  : "run_end",
                           "body"      : "",
                           "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
                           "end_time"  : end_time.strftime("%Y-%m-%d %H:%M:%S")}
            if not only_display:
                searching_on_clients_time = datetime.fromtimestamp(searching_on_clients_time)
                searching_on_indexers_time = datetime.fromtimestamp(searching_on_indexers_time)
                json_result.update({
                    "searching_on_clients_time" : searching_on_clients_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "searching_on_indexers_time": searching_on_indexers_time.strftime("%Y-%m-%d %H:%M:%S")
                })
            json_result.update(self._format_result(result))
            self.do_request(self.config.run_end, json_result)

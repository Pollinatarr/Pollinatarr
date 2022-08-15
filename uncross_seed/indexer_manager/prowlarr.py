#!/usr/bin/python3

from __future__ import annotations

import json
from typing import TYPE_CHECKING
from urllib.parse import urlencode

import requests

from uncross_seed.indexer_manager.abstract_indexer_manager import AbstractIndexerManager

if TYPE_CHECKING:
    from uncross_seed.config.indexer_managers_client_config import ProwlarrClientConfig


class ProwlarrClient(AbstractIndexerManager):
    def __init__(self, config: ProwlarrClientConfig):
        super().__init__(config)
    
    
    def search_by_name(self, _name: str, **opts):
        indexer_id = opts["indexer_id"]
        get_options = {
            "query"     : _name,
            "indexerIds": indexer_id
        }
        headers = {"Accept"      : "application/json",
                   "Content-Type": "application/json",
                   "X-Api-Key"   : self.api_key}
        request_url = f"{self.host}/api/v1/search?{urlencode(get_options)}"
        r = requests.get(request_url, headers=headers)
        json_data = json.loads(r.text)
        return json_data

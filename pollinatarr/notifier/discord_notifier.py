#!/usr/bin/python3

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from discord_webhook import DiscordWebhook, DiscordEmbed

from pollinatarr.notifier.abstract_notifier import AbstractNotifier

if TYPE_CHECKING:
    from pollinatarr.config.notifier_config import DiscordNotifierConfig


class DiscordNotifier(AbstractNotifier):
    def __init__(self, config: DiscordNotifierConfig):
        super().__init__(config)
        self.config = config
    
    
    def run_start(self, start_time, run_mode):
        if self.config.run_start:
            webhook = DiscordWebhook(url=self.config.run_start)
            
            embed = DiscordEmbed(title="", description="")
            embed.add_embed_field(name="Run mode", value=f"{run_mode}")
            embed.set_author(name="Pollinatarr : Starting detection")
            webhook.add_embed(embed)
            response = webhook.execute()
    
    
    def run_end(self, start_time, end_time, result, only_display, searching_on_clients_time=None, searching_on_indexers_time=None):
        if self.config.run_end:
            start_time = datetime.fromtimestamp(start_time)
            end_time = datetime.fromtimestamp(end_time)
            
            webhook = DiscordWebhook(url=self.config.run_start)
            
            embed = DiscordEmbed(title="", description="")
            embed.add_embed_field(name="Start time", value=f"{start_time.strftime('%Y-%m-%d %H:%M:%S')}")
            embed.add_embed_field(name="End time", value=f"{end_time.strftime('%Y-%m-%d %H:%M:%S')}")
            embed.set_author(name="Pollinatarr : Detection ended")
            
            if not only_display:
                searching_on_clients_time = datetime.fromtimestamp(searching_on_clients_time)
                searching_on_indexers_time = datetime.fromtimestamp(searching_on_indexers_time)
                embed.add_embed_field(name="Searching on clients time", value=f"{searching_on_clients_time} seconds")
                embed.add_embed_field(name="Searching on indexers time", value=f"{searching_on_indexers_time} seconds")
            
            webhook.add_embed(embed)
            response = webhook.execute()
            
            for torrent in result:
                webhook = DiscordWebhook(url=self.config.run_start)
                category = torrent.get("category", None) or "NO_CATEGORY"
                trackers = torrent.get('trackers', ())
                embed = DiscordEmbed(title=f"Torrent is missing from {len(trackers)} tracker(s)", description="")
                embed.add_embed_field(name="Torrent name", value=torrent.get("torrent_name", "MISSING NAME"), inline=False)
                tracker_text = '\n'.join(trackers)
                embed.add_embed_field(name="Category", value=category, inline=False)
                embed.add_embed_field(name="Trackers missing this", value=f"```{tracker_text}```", inline=False)
                embed.set_author(name="Pollinatarr")
                webhook.add_embed(embed)
                response = webhook.execute()

            pass

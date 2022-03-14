import asyncio
from logging import getLogger
from typing import Any, Dict, Optional

import discord

from . import plugin
from . import watchdog as watchdog

LOGGER = getLogger(__name__)


class g:
    default_prefix = '!'
    prefix_map: Dict[int, str] = {}

class Natsumi(discord.Client):

    def __init__(self,
                 *,
                 loop: Optional[asyncio.AbstractEventLoop] = None,
                 **options: Any):
        super().__init__(loop=loop, **options)
        plugin.reload()
        watchdog.start(plugin.g.path)
        
    async def _on_ready(self) -> None:
        plugin.reload()

    async def _on_message(self, message: discord.Message) -> None:
        prefix = g.default_prefix if isinstance(message.channel, discord.DMChannel) else g.prefix_map.get(message.guild.id) or g.default_prefix
        if message.content.startswith(prefix):
            command = message.content.split(' ')
            args = command[1:]
            command = command[0][len(prefix):].lower()
            for p in plugin.g.plugins.values():
                for a in p.aliases:
                    if command == a:
                        await p.execute(message, message.author, args)
                        break

    def dispatch(self, event: str, *args: Any, **kwargs: Any) -> None:
        super().dispatch(event, *args, **kwargs)
        method = 'on_' + event
        if method == 'on_message':
            self._schedule_event(self._on_message, method, *args, **kwargs)
        elif method == 'on_ready':
            self._schedule_event(self._on_ready, method, *args, **kwargs)
            
        for p in plugin.g.plugins.values():
            try:
                coro = getattr(p, method)
            except AttributeError:
                pass
            else:
                self._schedule_event(coro, method, *args, **kwargs)
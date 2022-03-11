import asyncio
from logging import getLogger
from typing import Any, Optional

import discord

from . import plugin
from . import watchdog as watchdog

LOGGER = getLogger(__name__)


class Natsumi(discord.Client):

    def __init__(self,
                 *,
                 loop: Optional[asyncio.AbstractEventLoop] = None,
                 **options: Any):
        super().__init__(loop=loop, **options)
        self.prefix = '!'
        plugin.reload()
        watchdog.start(plugin.g.path)
        
    async def _on_message(self, message: discord.Message) -> None:
        plugin.reload()

    async def _on_message(self, message: discord.Message) -> None:
        if message.content.startswith(self.prefix):
            command = message.content.split(' ')
            args = command[1:]
            command = command[0][len(self.prefix):]
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
        if method == 'on_ready':
            self._schedule_event(self._on_message, method, *args, **kwargs)
            
        for p in plugin.g.plugins.values():
            try:
                coro = getattr(p, method)
            except AttributeError:
                pass
            else:
                self._schedule_event(coro, method, *args, **kwargs)
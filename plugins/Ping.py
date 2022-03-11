from logging import getLogger
import natsucord
from discord import *
from typing import List

from natsucord import Command

LOGGER = getLogger(__name__)

class Ping(natsucord.CommandHandler):
    async def execute(self, message: Message, author: User, args: List[str]) -> None:
        await message.reply('Tomggg!')

class PingCommand(Command):
    def __init__(self) -> None:
        super().__init__('ping', 'test module', 'ping', ['ping', 'p'], Ping)
    
    async def on_reaction_add(self, reaction: Reaction, author: User) -> None:
        LOGGER.info('Reaction %s Added by %s' % (reaction.emoji, author))
    
    async def on_reaction_remove(self, reaction: Reaction, author: User) -> None:
        LOGGER.info('Reaction %s Removed by %s' % (reaction.emoji, author))


natsucord.plugin.register(__name__, PingCommand())
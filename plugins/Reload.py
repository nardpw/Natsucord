import natsucord
from discord import Message, User
from typing import List

from natsucord.command import Command

class Reload(natsucord.CommandHandler):
    async def execute(self, message: Message, author: User, args: List[str]) -> None:
        await message.reply('Reloading...')
        natsucord.plugin.reload()
        await message.reply('Done!')

natsucord.plugin.register(__name__, Command('ping', 'test module', '!ping', ['!reload', '!reload'], Reload))
import logging
import discord
import coloredlogs
import natsucord

LOGGER = logging.getLogger(__name__)

class Bot(natsucord.Client):
    
    async def on_ready(self) -> None:
        await super().on_ready()
        await self.change_presence(activity=discord.Game(name='なつみかん: natsumi#7504'))

if __name__ == '__main__':
    coloredlogs.install(level=logging.DEBUG)

    bot = Bot(intents = discord.Intents.all())
    bot.run('token')
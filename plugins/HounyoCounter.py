import natsucord
from discord import Message, User, TextChannel
from typing import Dict, List

from natsucord.command import Command, TypeCommand


class HounyoCounter(natsucord.CommandHandler):

    def __init__(self, channel: TextChannel, user: User) -> None:
        super().__init__(channel, user)
        self.count = 0

    async def execute(self, message: Message, author: User,
                      args: List[str]) -> None:
        self.count += 1
        await message.reply('hounyo count: %i' % self.count)
    
    def save(self) -> Dict:
        return {'count': self.count}

    @staticmethod
    def load(self: 'HounyoCounter', data: Dict) -> 'HounyoCounter':
        self.count = data['count']


natsucord.plugin.register(__name__,Command('HounyoCounter', 'count a your hounyo count', 'hounyo', ['hounyo', 'h'], HounyoCounter, 60, TypeCommand.USER))
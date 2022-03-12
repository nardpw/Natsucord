import asyncio
import json
import os
from enum import Enum
from time import time_ns
from typing import Dict, Generic, List, Type, TypeVar

import discord

class g:
    data_path = os.path.join(os.getcwd(), '.natsumicord')

class TypeCommand(Enum):
    STATIC = 0
    GUILD = 1
    CHANNEL = 2
    USER = 3
    DM = 4

class CommandHandler:
    def __init__(self, channel: discord.TextChannel, user: discord.User) -> None:
        self.channel = channel
        self.user = user

    async def execute(self, message: discord.Message, author: discord.User, args: List[str]) -> None:
        ...
    
    def save(self) -> Dict:
        ...
    
    @staticmethod
    def load(self, data: Dict) -> 'CommandHandler':
        ...

class Command:

    def __init__(self,
                 name: str,
                 desc: str,
                 usage: str,
                 aliases: List[str],
                 handler: type[CommandHandler] = CommandHandler,
                 timeout: int = 5,
                 type: TypeCommand = TypeCommand.STATIC) -> None:
        self.name: str = name
        self.desc: str = desc
        self.usage: str = usage
        self.aliases: List[str] = aliases
        self.handler: CommandHandler = handler
        self.timeout: int = timeout
        self.type: TypeCommand = type
        self.instance: CommandHandler = handler(None, None)
    
    def _get_instance(self, id_: str, *args) -> CommandHandler:
        id_ += '.json'
        dir_ = os.path.join(g.data_path, self.name)
        os.makedirs(dir_, exist_ok=True)
        path_ = os.path.join(dir_, id_)
        r = None
        if os.path.exists(path_) and os.path.isfile(path_):
            with open(path_) as f:
                obj = json.load(f)
            r = self.handler(*args)
            self.handler.load(r, obj)
        else:
            r = self.handler(*args)
        return r
    
    def _save_instance(self, id_: str, instance: CommandHandler) -> None:
        id_ += '.json'
        data = instance.save()
        if data:
            dir_ = os.path.join(g.data_path, self.name)
            os.makedirs(dir_, exist_ok=True)
            path_ = os.path.join(dir_, id_)
            try:
                with open(path_, 'w') as f:
                    json.dump(data, f)
            except:
                os.remove(path_)


    async def execute(self, message: discord.Message, author: discord.User, args: List[str]) -> None:
        id_: str = None

        match self.type:
            case TypeCommand.STATIC:
                id_ = 'main'
            case TypeCommand.GUILD:
                id_ = str(message.guild.id)
            case TypeCommand.CHANNEL:
                id_ = str(message.channel.id)
            case TypeCommand.DM:
                id_ = str(message.author.dm_channel.id)
            case TypeCommand.USER:
                id_ = str(message.author.id)

        instance = self._get_instance(id_, message.channel, message.author)
        await asyncio.wait_for(instance.execute(message, author, args), timeout=self.timeout)
        self._save_instance(id_, instance)
        del instance
import asyncio

import discord
from discord.ext import commands

from dischatbot.constants import Bot as BotConfig

class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def create(cls) -> "Bot":
        """Create and return an instance of a Bot."""
        loop = asyncio.get_event_loop()
        intents = discord.Intents.default()
        intents.members = True

        return cls(
            loop=loop,
            intents=intents,
            command_prefix=commands.when_mentioned_or(BotConfig.prefix),
            activity=discord.Game(name=f"Commands: {BotConfig.prefix}help"),
            case_insensitive=True,
            max_messages=10_000,
        )

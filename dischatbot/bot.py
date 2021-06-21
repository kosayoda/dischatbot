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

        return cls(
            loop=loop,
            command_prefix=commands.when_mentioned_or(BotConfig.prefix),
            activity=discord.Game(name=f"Commands: {BotConfig.prefix}help"),
            case_insensitive=True,
            max_messages=10_000,
        )

    def load_extensions(self) -> None:
        """Load all enabled extensions."""
        extensions = []
        for extension in extensions:
            self.load_extension(extension)

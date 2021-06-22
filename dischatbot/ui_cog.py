from discord import Message
from discord.ext.commands import Bot, Cog

from dischatbot.ui import Application

class UI(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.ui = Application(bot=bot)
        self.bot.loop.create_task(self.init_ui())

    async def init_ui(self):
        await self.ui.run_async()

    @Cog.listener()
    async def on_message(self, message: Message):
        if message.author.bot:
            return
        await self.ui.show_message(message)

def setup(bot: Bot) -> None:
    """Loads the UI Cog."""
    bot.add_cog(UI(bot))

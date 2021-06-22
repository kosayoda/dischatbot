from discord import Message
from discord.ext.commands import Bot, Cog

from dischatbot.ui import Application, SystemMessage

class UI(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.ui = Application(bot=bot)
        self.bot.loop.create_task(self.init_ui())

    async def init_ui(self):
        await self.bot.wait_until_ready()
        await self.ui.init()
        await self.ui.run_async()

    @Cog.listener()
    async def on_message(self, message: Message):
        author = message.author
        if author.bot or not author:
            return

        if author.id != self.ui.current_chat.user_id:
            text = message.content
            text = f"{text[:20]}..." if len(text) > 20 else text
            self.ui.send_system_message(f"New message from {author} ({author.id}): {text}", SystemMessage.INFO)
            return

        await self.ui.update_chat(message=message)

def setup(bot: Bot) -> None:
    """Loads the UI Cog."""
    bot.add_cog(UI(bot))

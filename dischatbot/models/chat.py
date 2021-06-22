import asyncio
import typing as t

from discord import User, Message

from dischatbot.bot import Bot

class UnknownUser(Exception):
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id


class Chat:
    def __init__(self, bot: Bot, user_id: int):
        self.bot = bot
        self.messages = []
        self.user_id = user_id

        self.recipient: t.Optional[User] = self.bot.get_user(user_id)
        if (self.recipient is None):
            raise UnknownUser(user_id)

    async def populate_messages(self):
        async for message in self.recipient.history(limit=25):
            if not message.content:
                continue
            self.messages.append(message)

    def add_message(self, message):
        self.messages.append(message)

    def __str__(self):
        return "".join(reversed([self.format_message(msg) for msg in self.messages]))

    @staticmethod
    def format_message(msg: Message):
        user = str(msg.author)
        text = msg.content.strip()
        return f"{user:15}| {text}\n"

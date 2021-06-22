import asyncio
import enum
import inspect
import typing as t

import prompt_toolkit

from discord import Message
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.document import Document
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import TextArea, Label, HorizontalLine, Box

from dischatbot.bot import Bot
from dischatbot.models.chat import Chat

class SystemMessage(enum.Enum):
    INFO = "[ INFO  ]"
    ERROR = "[ ERROR ]"


# -- Keybindings --
kb = KeyBindings()
@kb.add("c-c")
def _(event):
    event.app.exit()

USER_ID = 180853534617632768

class Application(prompt_toolkit.Application):
    HELP_TEXT = """Welcome to dischatbot. Run /help for a list of commands."""

    def __init__(self, *args, **kwargs):
        self.bot: Bot = kwargs.pop("bot")

        self.chats = {}
        self.current_chat = None
        
        self.chat_window = TextArea()
        self.input_field = TextArea(height=1, prompt=">>> ", multiline=False, wrap_lines=True)
        self.input_field.accept_handler = self.get_input_handler()
        self.system_window = TextArea(height=5)

        self.layout = Layout(
            Box(
                HSplit([self.chat_window, HorizontalLine(), self.system_window, HorizontalLine(), self.input_field]),
                padding = 2
            ),
            focused_element=self.input_field,
        )

        super().__init__(*args, **kwargs, layout=self.layout, key_bindings=kb, full_screen=True)

    def get_input_handler(self):
        def accept(buffer: Buffer):
            user_input = buffer.text.strip()
            if not user_input:
                return
            if user_input.startswith("/") and not user_input.startswith("//"):
                command, sep, argument = user_input[1:].partition(" ")
                try:
                    command_func = getattr(self, f"do_{command}")
                except AttributeError:
                    self.send_system_message(f"Unknown command: {command}", SystemMessage.ERROR)
                else:
                    if inspect.iscoroutinefunction(command_func):
                        asyncio.create_task(command_func(argument))
                    else:
                        command_func(argument)
                    return

            if self.current_chat is not None:
                asyncio.create_task(self.do_chat(self.current_chat.user_id, user_input))
            else:
                self.send_system_message(f"Unknown message: {user_input}", SystemMessage.ERROR)


        return accept

    async def init(self):
        self.send_system_message(self.HELP_TEXT, SystemMessage.INFO)
    
    async def do_chat(self, user_id: t.Union[str, int], message: str = None):
        if isinstance(user_id, str):
            user_id = int(user_id)

        if self.chats.get(user_id) is None:
            self.chats[user_id] = Chat(self.bot, user_id)
            await self.chats[user_id].populate_messages()

        chat: Chat = self.chats[user_id]
        self.current_chat = chat

        if message is not None:
            msg = await chat.recipient.send(message)
            await self.update_chat(msg)
        else:
            await self.update_chat()
            self.send_system_message(f"Now connected to: {chat.recipient}", SystemMessage.INFO)

    async def update_chat(self, message: Message = None):
        if message is None:
            text = str(self.current_chat)
            self.chat_window.buffer.document = Document(text=text, cursor_position=len(text))
        else:
            text = self.current_chat.format_message(message)
            self.chat_window.buffer.insert_text(text)

    async def display_chat(self, text: str):
        self.chat_window.buffer.insert_text(text)

    def send_system_message(self, message: str, message_type: SystemMessage):
        self.system_window.buffer.insert_text(f"{message_type.value} {message}\n")

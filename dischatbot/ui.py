import asyncio

import prompt_toolkit

from discord import Message
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.document import Document
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import TextArea, Label, HorizontalLine

from dischatbot.bot import Bot

kb = KeyBindings()
@kb.add("c-c")
def _(event):
    event.app.exit()


class Application(prompt_toolkit.Application):
    def __init__(self, *args, **kwargs):
        self.bot: Bot = kwargs.pop("bot")
        
        self.chat_window = TextArea(text="Started!")
        self.input_field = TextArea(height=1, prompt=">>> ", multiline=False, wrap_lines=False)
        self.input_field.accept_handler = self.get_input_handler()

        self.layout = Layout(HSplit([self.chat_window, HorizontalLine(), self.input_field]), focused_element=self.input_field)

        super().__init__(*args, **kwargs, layout=self.layout, key_bindings=kb, full_screen=True)

    def get_input_handler(self):
        def accept(buffer: Buffer):
            async def send_message(msg):
                # await self.bot.get_user(<user>).send(msg)
                pass

            new_text = f"{self.chat_window.text}\n>>> {buffer.text}"
            self.chat_window.buffer.document = Document(text=new_text, cursor_position=len(new_text))
            asyncio.create_task(send_message(buffer.text))

        return accept
    
    async def show_message(self, message: Message):
        new_text = f"{self.chat_window.text}\n{str(message.author):^10} | {message.content}"
        self.chat_window.buffer.document = Document(text=new_text, cursor_position=len(new_text))

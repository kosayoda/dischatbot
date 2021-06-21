from discord import Game
from discord.ext.commands import Bot

import dischatbot as bot
from dischatbot.bot import Bot
from dischatbot.constants import Bot as BotConfig
 

bot.instance = Bot.create()
bot.instance.load_extensions()
bot.instance.run(BotConfig.token)

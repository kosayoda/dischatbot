from discord import Game

import dischatbot as bot
from dischatbot.bot import Bot
from dischatbot.constants import Bot as BotConfig
 

def main() -> None:
    bot.instance = Bot.create()
    bot.instance.load_extension("dischatbot.ui_cog")
    bot.instance.run(BotConfig.token)

if __name__ == "__main__":
    main()

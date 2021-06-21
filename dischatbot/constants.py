from typing import NamedTuple
from os import environ

try:
    import dotenv
    dotenv.load_dotenv()
except ModuleNotFoundError:
    pass

__all__ = (
    "Bot", "Channels",
)

class Bot(NamedTuple):
    guild = int(environ.get("GUILD", 549043330168782868))
    prefix = environ.get("PREFIX", "|")
    token = environ.get("TOKEN")
    debug = environ.get("DEBUG", "").lower() == "true"

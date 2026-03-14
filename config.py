import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID", "0"))
BOT_COLOR = int(os.getenv("BOT_COLOR", "0xE02D60"), 16)
API_BASE_URL = os.getenv("API_BASE_URL", "https://datafansub.bye.moe/api")
ANILIST_URL = os.getenv("ANILIST_URL", "https://graphql.anilist.co")
DATAFANSUB_URL = os.getenv("DATAFANSUB_URL", "https://datafansub.bye.moe")

ANIMES_URL = f"{API_BASE_URL}/collections/animes/records"
FANSUBS_URL = f"{API_BASE_URL}/collections/fansubs/records"
ENTRIES_URL = f"{API_BASE_URL}/collections/entries/records"
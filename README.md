# Shinobu Bot

Discord bot for searching animes in the DataFansub database directly from Discord. Integrates with AniList to fetch additional information like posters, titles in different languages, and release year.

## Features

- **Anime Search**: Search animes on DataFansub with autocomplete
- **Season Selection**: Interactive interface to select seasons
- **AniList Integration**: Shows posters, romaji/english/native titles, and release year
- **Auto-caching**: Updates data every 5 minutes for faster responses
- **Slash Commands**: Modern Discord command system

## Commands

| Command | Description |
|---------|-------------|
| `/datafansub` | Search for an anime on DataFansub and display fansub info, status, Nyaa and NekoBT links |
| `/ping` | Show bot latency |
| `/help` | List all available commands |

## Requirements

- Python 3.9+
- Discord Bot Token
- Access to DataFansub API
- Access to AniList API (optional)

## Installation

### Local

1. Clone the repository:
```bash
git clone https://github.com/ougihz/shinobu-bot.git
cd shinobu-bot
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables in `.env`:
```env
TOKEN=your_discord_token
WELCOME_MESSAGE=Welcome message
GUILD_ID=server_id
BOT_COLOR=0xE02D60
API_BASE_URL=https://datafansub.bye.moe/api
ANILIST_URL=https://graphql.anilist.co
DATAFANSUB_URL=https://datafansub.bye.moe
```

5. Run the bot:
```bash
python main.py
```

### Docker

1. Configure the `.env` file with your variables
2. Build and run:
```bash
docker-compose up -d
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `TOKEN` | Your Discord bot token | - |
| `GUILD_ID` | Discord server ID | - |
| `WELCOME_MESSAGE` | Welcome message | - |
| `BOT_COLOR` | Embed color in hexadecimal | `0xE02D60` |
| `API_BASE_URL` | DataFansub API URL | `https://datafansub.bye.moe/api` |
| `ANILIST_URL` | AniList API URL | `https://graphql.anilist.co` |
| `DATAFANSUB_URL` | DataFansub main URL | `https://datafansub.bye.moe` |

## Project Structure

```
shinobu-bot/
├── main.py              # Bot entry point
├── config.py            # Configuration and environment variables
├── api.py               # Functions to interact with external APIs
├── commands/
│   └── general.py       # Bot commands
├── Dockerfile           # Docker image
├── docker-compose.yml   # Docker orchestration
└── requirements.txt     # Python dependencies
```

## Technologies

- [discord.py](https://discordpy.readthedocs.io/) - Library for creating Discord bots
- [aiohttp](https://docs.aiohttp.org/) - Asynchronous HTTP client
- [python-dotenv](https://pypi.org/project/python-dotenv/) - Environment variable loading
- [AniList API](https://anilist.gitbook.io/anilist-apiv2-docs/) - Anime information

## License

This project is private and not open source. All rights reserved.

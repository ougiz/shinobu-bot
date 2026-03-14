import discord
from discord.ext import commands, tasks
import config
import api
from commands.general import datafansub, ping, help_command


intents = discord.Intents.all()
guild = discord.Object(id=config.GUILD_ID)

bot = commands.Bot(command_prefix="", intents=intents)


@tasks.loop(minutes=5)
async def refresh_caches():
    await api.refresh_caches()


@bot.event
async def on_ready():
    print(f"Bot connected as: {bot.user}")
    refresh_caches.start()

    await bot.tree.sync()
    await bot.tree.sync(guild=guild)
    print("Commands synced globally and in guild")


bot.tree.add_command(datafansub)
bot.tree.add_command(ping)
bot.tree.add_command(help_command)

bot.run(config.TOKEN)
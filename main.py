import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
import random
import logging
import emoji
import os

# Setting up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
file_handler = logging.FileHandler('bot.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Instantiate the bot object and set options variables
intents = discord.Intents().all()
bot = commands.Bot(command_prefix='.', intents=intents)
YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True', 'limitrate:': '4.2M'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
DISCORD_SECRET = os.getenv("DISCORD_SECRET")

# Cog extensions list
extensions = ['cogs.administrator',
              'cogs.entertainment',
              'cogs.voicebot',
              'cogs.odinsgame',
              'cogs.bank']


def load_extensions(ext_list: list):
    """Load extensions, skip and log if they fail"""
    loaded_exts = []
    for ext in ext_list:
        try:
            bot.load_extension(ext)
            loaded_exts.append(ext)
        except Exception as e:
            logger.warning(f'{e} \n Failed to load extension "{ext}". Skipped')
    logger.info('Bot Loaded with extensions : ' + ' : '.join(loaded_exts))


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name='www.github.com/odinmay'))
    logger.info('Bot is online and ready')


@bot.event
async def on_member_join(member):
    print(f'hello {member}')
    logger.info('Member join function called')


@bot.event
async def on_member_remove(member):
    print(f'{member} has left the server')


if __name__ == '__main__':
    load_extensions(extensions)
    bot.run(DISCORD_SECRET)

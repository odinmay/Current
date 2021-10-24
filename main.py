"""This is the main bot file which is executed and handles
   connecting to Discord bot application and loading cogs"""

import logging
import os
import discord
from discord.ext import commands
from discord.ext.commands import ExtensionFailed
from discord.utils import get


# Setting up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)s:%(asctime)s:%(levelname)s:%(message)s')
file_handler = logging.FileHandler('bot.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Instantiate the bot object and set options variables
intents = discord.Intents().all()
bot = commands.Bot(command_prefix='.', intents=intents)
YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True', 'limitrate:': '4.2M'}
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
    }

DISCORD_SECRET = os.getenv("DISCORD_SECRET")

# Cog extensions list
extensions = ['cogs.administrator',
              'cogs.entertainment',
              'cogs.voicebot',
              'cogs.cardsagainstdiscord',
              'cogs.bank',
              'cogs.games',
              'cogs.aku']


def load_extensions(ext_list: list):
    """Load extensions, skip and log if they fail"""
    loaded_exts = []
    for ext in ext_list:
        try:
            bot.load_extension(ext)
            loaded_exts.append(ext)
        except ExtensionFailed as err:
            logger.warning('%s \n Failed to load extension "%s". Skipped', err, ext)
    loaded_exts = ' : '.join(loaded_exts)
    logger.info('Bot Loaded with extensions : %s', loaded_exts)


@bot.event
async def on_ready():
    """Once the bot has fully loaded this is called and sets the bots activity"""
    await bot.change_presence(activity=discord.Game(name='github.com/odinmay'))
    logger.info('Bot is online and ready')


@bot.event
async def on_member_join(member):
    """When a member joins the server the bot will give them a role"""
    role = get(member.guild.roles, id=285629786532085761)
    await member.add_roles(role)
    logger.info('%s has joined the server. Role assigned.', str(member))


if __name__ == '__main__':
    load_extensions(extensions)
    bot.run(DISCORD_SECRET)

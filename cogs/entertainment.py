"""The entertainment Cog, games, media, and memes live here."""

import logging
import random
import json
import requests
from discord.ext import commands
from discord import Spotify
import discord
from .bank import query_db



logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(name)s:%(asctime)s:%(levelname)s:%(message)s')
file_handler = logging.FileHandler('bot.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Helper Functions #

def translate_sindarin(text):
    """GET Api data and return it"""
    url = 'https://api.funtranslations.com/translate/sindarin.json'
    querystring = {'text': text}
    response = requests.get(url, params=querystring)
    try:
        return response.json()['contents']['translated']
    except KeyError:
        return response.json()['error']['message']


def pull_joke():
    """GET Api data and return it"""
    url = "https://joke3.p.rapidapi.com/v1/joke"
    headers = {
        'x-rapidapi-host': "joke3.p.rapidapi.com",
        'x-rapidapi-key': "006adefbccmshf086e0b885be71bp1c8a29jsnbf24cc6763f4"
    }
    response = requests.request("GET", url, headers=headers)
    return response.json()['content']


def pull_chucknorris():
    """GET Api data and return it"""
    req = requests.get('https://api.chucknorris.io/jokes/random')
    return req.json()['value']


def scryfall(card_name):
    """GET Api data and return it"""
    url = 'https://api.scryfall.com/cards/search'
    querystring = {'q': card_name}
    response = requests.request('GET', url, params=querystring)
    try:
        return json.loads(response.text)['data'][0]['image_uris']['normal']
    except:
        return 'Card not in either database'


def scryfall_art(card_name):
    """GET Api data and return it"""
    url = 'https://api.scryfall.com/cards/search'
    querystring = {'q': card_name}
    response = requests.request('GET', url, params=querystring)
    try:
        return json.loads(response.text)['data'][0]['image_uris']['art_crop']
    except:
        return 'Cropped card art unavailable for this card sorry.'


def scryfall_price(card_name):
    """GET Api data and return it"""
    url = 'https://api.scryfall.com/cards/search'
    querystring = {'q': card_name}
    response = requests.request('GET', url, params=querystring)
    try:
        prices = json.loads(response.text)['data'][0]['prices']
        price_list = list(prices.items())
        msg = f'{price_list[0][0]} : {price_list[0][1]} \n{price_list[1][0]} : {price_list[1][1]}'
        return msg
    except:
        return 'Card price not in either database'


def pull_mtgio_card(card_name):
    """GET Api data and return it"""
    url = 'https://api.magicthegathering.io/v1/cards'
    querystring = {'name': card_name}
    response = requests.request('GET', url, params=querystring)
    try:
        return response.json()['cards'][0]['imageUrl']
    except:
        return scryfall(card_name)


def pull_movie(movie):
    """GET Api data, create embed message and return it"""
    url = f"https://imdb-internet-movie-database-unofficial.p.rapidapi.com/film/{movie}"
    headers = {
        'x-rapidapi-host': "imdb-internet-movie-database-unofficial.p.rapidapi.com",
        'x-rapidapi-key': "006adefbccmshf086e0b885be71bp1c8a29jsnbf24cc6763f4"
    }
    response = requests.request("GET", url, headers=headers).json()

    embed_msg = discord.Embed(title=f"{str(movie).title()} | {response['rating']}/10",
                             description=f"{response['plot']}",
                             url=response['trailer']['link'],
                             color=0x00C7FF
                             )
    embed_msg.set_image(url=response['poster'])
    return embed_msg


class Entertainment(commands.Cog):
    """The Entertainment Cog Class, commands live here."""
    def __init__(self, bot):
        self.bot = bot
        self.strikes = 0

    @commands.command(name='8ball')
    async def _8ball(self, ctx, *, question):
        """Ask it a question!"""
        responses = ["It is certain.",
                     "It is decidedly so.",
                     "Without a doubt.",
                     "Yes - definitely.",
                     "You may rely on it.",
                     "As I see it, yes.",
                     "Most likely.",
                     "Outlook good.",
                     "Yes.",
                     "Signs point to yes.",
                     "Reply hazy, try again.",
                     "Ask again later.",
                     "Better not tell you now.",
                     "Cannot predict now.",
                     "Concentrate and ask again.",
                     "Don't count on it.",
                     "My reply is no.",
                     "My sources say no.",
                     "Outlook not so good.",
                     "Very doubtful."]
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

    @commands.command(aliases=['coin'])
    async def flip(self, ctx):
        """Whats the most you ever lost in a coin toss?"""
        await ctx.send(random.choice(['Heads', 'Tails']))

    @commands.command()
    async def joke(self, ctx, user: discord.Member = None):
        """Tells a joke"""
        user = user or ctx.author
        await ctx.send(pull_joke())

    @commands.command(aliases=['chuck norris', 'chucknorris', 'norris'])
    async def chuck(self, ctx, user: discord.Member = None):
        """Tells a Chuck Noris FACT."""
        user = user or ctx.author
        await ctx.send(pull_chucknorris())

    @commands.command(aliases=['magic', 'magician'])
    async def magicians(self, ctx):
        """Displays random Magicians gif"""
        with open('magicians_urls.txt', 'r', encoding='utf-8') as file:
            data = file.read()
            await ctx.send(random.choice(data.split(',')))

    @commands.command()
    async def mtg(self, ctx, *, card):
        """Magic The Gathering card data from magicthegathering.io/scryfall"""
        async with ctx.message.channel.typing():
            await ctx.send(pull_mtgio_card(card))
            await ctx.send(scryfall_price(card))

    @commands.command()
    async def mtg_art(self, ctx, *, card):
        """Magic The Gathering card art from magicthegathering.io/scryfall"""
        async with ctx.message.channel.typing():
            await ctx.send(scryfall_art(card))

    @commands.command()
    async def movie(self, ctx, *, movie):
        """Displays a movies plot/rating/trailer"""
        await ctx.send(embed=pull_movie(movie))

    @commands.command()
    async def sindarin(self, ctx, *, text):
        """Translates message into Elvish(Sindarin)"""
        await ctx.send(translate_sindarin(text))

    @commands.command()
    async def spotify(self, ctx, user: discord.Member = None):
        """Shares what you are listening to on Spotify"""
        user = user or ctx.author
        for activity in user.activities:
            if isinstance(activity, Spotify):
                await ctx.send(
                    f"{user} is listening to {activity.title} by"
                    f" {activity.artist} {activity.album_cover_url}")

    @commands.command(aliases=['defelcts'])
    async def deflect(self, ctx) -> str:
        """Displays a random deflect gif"""
        await ctx.send(random.choice(
            ['https://media2.giphy.com/media/l1KVaixq8xLxoHEti/giphy.gif',
             'https://media4.giphy.com/media/3ohjUQ81edgmV8Gu40/giphy.gif',
             'https://i.imgur.com/zPSpCpD.gif',
             'https://thumbs.gfycat.com/EllipticalSophisticatedHorsemouse-size_restricted.gif',
             'https://media.tenor.com/images/8ea0b658e77683528a151deef9154e94/tenor.gif',
             'https://media.tenor.com/images/0802de3dbf808ae7f1e13185f5bcb15a/tenor.gif',
             'https://media3.giphy.com/media/9dhFwjb4adknC/giphy.gif']))


    @commands.command()
    async def join_ss(self, ctx):
        """Adds a player to the secret santa table if they aren't already in it"""
        user = ctx.author.name
        query = f"SELECT `name` FROM `secret_santas` WHERE `name` = '{user}'"
        results = query_db(query)
        if results:
            await ctx.send(f"{user} has already joined Secret Santa.")
        else:
            query = f"INSERT INTO `secret_santas`(`name`, `id`) VALUES ('{ctx.author.name}', '{str(ctx.author.id)}')"
            result = query_db(query)
            await ctx.send(f"{user} has joined Secret Santa with id: {ctx.author.id}")

    @commands.command()
    async def draw_ss(self, ctx):
        """Randomly pairs names from DB and dm's them their partner"""
        query = f"SELECT * FROM `secret_santas`"
        results = query_db(query)

        name_list = [(result[0], result[1]) for result in results]
        name_list_copy = name_list.copy()

        for name in name_list:
            partner = random.choice(name_list_copy)
            while name == partner:
                partner = random.choice(name_list_copy)

            #SEND DM
            member = await ctx.guild.fetch_member(int(name[1]))
            channel = await member.create_dm()
            await channel.send(f"Please buy a steam game for {partner[0]}. The price limit is $20 Please don't feel obligated to spend the whole $20. You can buy a $2 game. Merry Christmas!")
            name_list_copy.remove(partner)

        query = f"TRUNCATE TABLE `secret_santas`"
        query_db(query)

def setup(bot):
    """Called to initialize Cog to the bot"""
    bot.add_cog(Entertainment(bot))

from asyncio import sleep
from discord.ext import commands
import data_compile
import discord
import datetime
import random
import emoji
from bank import Bank

emoji_list = [':one:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:']
question_list = ['I cant believe you like _____ too, we should hang out.']


class OdinsGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game = Game()

    @commands.command()
    async def game_join(self, ctx):
        self.game.players.update({ctx.author.name: Player(ctx.author.name, len(self.game.players), ctx.author)})
        self.game.channel = ctx.message.channel
        if not self.game.started:
            self.game.status = 'Players are still able to join, to start with current players do .prompt'
            await ctx.send(f'{ctx.author} has joined the game! \n'
                           f'{len(self.game.players)} people are playing this round.')
        else:
            await ctx.send('The game has already started. Wait until next round to join.')

    @commands.command()
    async def game_start(self, ctx):
        # set min players
        if len(self.game.players) > 0:
            self.game.question = random.choice(data_compile.master_list)

            for player in self.game.players:
                channel = await self.game.players[player].member.create_dm()
                await channel.send(self.game.question)
            self.game.status = 'A prompt was give, voting is in process. Vote with ---->  .vote response'
            self.game.started = True
        else:
            await ctx.send('Not enough players to start the game. Minimum is ')

    @commands.command()
    async def vote(self, ctx, *, players_response):
        self.game.players[ctx.author.name].id = self.game.total_responses
        self.game.players[ctx.author.name].response = players_response
        self.game.players[ctx.author.name].vote = Vote(self.game.total_responses)
        await ctx.send('Vote Registered. Check back in the discord for scoring!')
        self.game.total_responses += 1
        # Check if all votes are submitted
        if self.game.total_responses == len(self.game.players):
            await ctx.send('All Votes Cast, please vote in the Discord Server.')
            self.game.response_message = await self.game.channel.send(self.game.question + '\n' + self.create_message())
        # Adds Reactions to formattedd message
        for player in self.game.players:
            # This might break because players will not be in order
            await self.game.response_message.add_reaction(
                f"{self.game.players[player].id + 1}\N{COMBINING ENCLOSING KEYCAP}")
        # waits duration and calls decide winner
        await self.wait_for_results()

    def create_message(self):
        # Takes all the player responses and creates a message and a unique emote number for each
        return_msg = ''
        for key, player in enumerate(self.game.players):
            return_msg += emoji_list[key] + ' ' + self.game.players[player].response + '\n'
        return return_msg

    async def wait_for_results(self):
        '''Delays game for voting, counts reactions, and calls decide_winner(react_info)'''
        await sleep(5)
        await self.game.channel.send('Voting concludes in 5 seconds')
        await sleep(5)
        cached_msg = discord.utils.get(self.bot.cached_messages, id=self.game.response_message.id)
        reactions_tally = []
        highest = 0
        for x in cached_msg.reactions:
            for player in self.game.players:
                self.game.players[player].id = x

        # for react in cached_msg.reactions:
        #     reactions_tally.append(react)
        for player in self.game.players:
            if self.game.players[player].id.count > highest:
                self.game.winner = self.game.players[player].name
            else:
                continue
        await self.game.channel.send(
            f'{self.game.winner} Has Won the Round!\n Awarded {len(self.game.players) * 10} dollars')
        Bank.add_money(self.game.winner, len(self.game.players) * 10)
        await self.again(self.game.channel)

    async def again(self, channel):
        msg = await channel.send('Play another round?')
        await msg.add_reaction(':white_check_mark:')
        await msg.add_reaction(emoji='816481343624970340')
        await sleep(5)
        cached_msg = discord.utils.get(self.bot.cached_messages, id=msg.id)
        for emoji1, emoji2 in cached_msg.reactions:
            print(emoji1, emoji2)


def setup(bot):
    bot.add_cog(OdinsGame(bot))


class Game:
    """Game object containing state, players, game data etc.
    One of these per round is instantiated, new one made on .game_reset"""

    def __init__(self):
        self.players = {}
        self.started = False
        self.status = ''
        self.total_responses = 0
        self.response_message = ''
        self.channel = None
        self.reactions = []
        self.winner = None
        self.question = None


class Vote:
    """Object for vote, contains data linking to players and their response"""

    def __init__(self, id):
        self.id = id


class Player():
    """Player object used to hold players info"""

    def __init__(self, name, id, member):
        self.name = name
        self.response = {}
        self.id = id
        self.vote = None
        self.member = member

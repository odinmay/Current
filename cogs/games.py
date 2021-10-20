from discord.ext import commands
import random
from .bank import Bank


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def guess(self, ctx, *, guess):
        """Guess a number 1-100. Win $200 if you hit it"""
        number = random.randint(1, 100)

        if int(guess) == number:
            await ctx.send(Bank.add_money(ctx.author.name, 200))
        else:
            await ctx.send(f'You guessed {guess}. The number was {number}. Sorry')

    @commands.command()
    async def beg(self, ctx):
        """Beg for a small amount of cash"""
        number = random.randint(1, 5)
        await ctx.send(Bank.add_money(ctx.author.name, number))


def setup(bot):
    bot.add_cog(Games(bot))

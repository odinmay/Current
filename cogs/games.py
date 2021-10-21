import discord
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

    @commands.command()
    async def bet(self, ctx, *, bet):
        """1% chance for 8x, 30% chance for 2x payout"""
        number = random.randint(1, 100)
        if number == random.randint(1, 100):
            Bank.add_money(ctx.author.name, bet * 8)
            await ctx.send(f"*** CONGRATS! SUPER JACKPOT!!!!  8x PAYOUT!!***")
        elif number < 31:
            Bank.add_money(ctx.author.name, int(bet) * 2)
            await ctx.send(f"Winner Winner! You won ${int(bet) * 2}")
        else:
            Bank.sub_money(ctx.author.name, bet)
            await ctx.send(f"Unlucky! You lost ${bet}. Try again?")

    @commands.command()
    async def steal(self, ctx, member: discord.Member):
        """Attempt to steal $150 from a members account"""
        number = random.randint(1,100)
        if number > 60:
            await ctx.send(f"You successfully stole ${150} from {member}.")
            await ctx.send(Bank.add_money(ctx.author.name, 150))
            Bank.sub_money(member.name, 150)
        else:
            await ctx.send(f"You failed to steal from {member}.")

def setup(bot):
    bot.add_cog(Games(bot))

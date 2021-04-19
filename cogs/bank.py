from discord.ext import commands
import discord
import os
import json


class Bank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def reset_all_accounts():
        with open("accounts.json", "r") as f:
            users = json.load(f)

        for k, v in users.items():
            users[k] = 0

        with open("accounts.json", mode="w") as f:
            json.dump(users, f)

    @staticmethod
    def add_money(name, amount):
        with open("accounts.json", "r") as f:
            users = json.load(f)

        if name in users:
            users[name] += int(amount)
            with open("accounts.json", "w") as f:
                json.dump(users, f)
        else:
            users[name] = 0
            users[name] += int(amount)
            with open("accounts.json", "w") as f:
                json.dump(users, f)

    @staticmethod
    def sub_money(name, amount):
        with open("accounts.json", "r") as f:
            users = json.load(f)

        if name in users:
            return False
        else:
            users[name] = 0

        users[name] -= amount
        with open("accounts.json", "w") as f:
            json.dump(users, f)

    async def get_account_data(self):
        with open("accounts.json", "r") as f:
            users = json.load(f)
        return users

    async def open_account(self, user):
        users = await self.get_account_data()
        print(users)
        if str(user.name) in users:
            return False
        else:
            users[str(user.name)] = 0
        with open("accounts.json", "w") as f:
            json.dump(users, f)
        return True

    @commands.command(aliases=['b', 'bal'], description='Checks your bank account')
    async def balance(self, ctx):
        users = await self.get_account_data()
        await self.open_account(ctx.author)
        name = ctx.author.name
        bal = users[name]
        await ctx.send(f'{name} your balance is {bal}')

    # @commands.command()
    # async def test(self,ctx,amount):
    #     await Bank.add_money(ctx.author.name, amount)
    #     await self.balance(ctx)

    # @commands.command(description='A place to spend your money!',aliases=['s'])
    # async def shop(self,ctx):
    #     '''View commands to buy things'''
    #     pass


def setup(bot):
    bot.add_cog(Bank(bot))

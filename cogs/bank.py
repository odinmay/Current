import os
from discord.ext import commands
from mysql.connector import connect, Error

host = os.getenv()
user = os.getenv()
password = os.getenv()
database = os.getenv()


class Bank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def has_account(name):
        """Checks if the name is in DB"""
        query = f"SELECT `user` FROM `accounts` WHERE `user` = '{name}'"

        try:
            with connect(
                    host=host,
                    user=user,
                    password=password,
                    database=database
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    results = cursor.fetchall()
                    if len(results) > 0:
                        return True
                    else:
                        return False
                    connection.commit()
        except Error as e:
            print(e)

    @staticmethod
    def add_money(name, amount):
        """Adds money to an account"""
        if not Bank.has_account(name):
            Bank.open_account(name)

        add_query = f"UPDATE `accounts` SET `balance` = balance + {amount} WHERE `user` = '{name}'"

        try:
            with connect(
                    host=host,
                    user=user,
                    password=password,
                    database=database
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(add_query)
                    connection.commit()
                    return f"${amount} Added to {name}'s account."
        except Error as e:
            print(e)

    @staticmethod
    def sub_money(name, amount):
        """Subtracts money from an account"""
        if not Bank.has_account(name):
            Bank.open_account(name)

        add_query = f"UPDATE `accounts` SET `balance` = balance - {amount} WHERE `user` = '{name}'"

        try:
            with connect(
                    host=host,
                    user=user,
                    password=password,
                    database=database
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(add_query)
                    connection.commit()
                    return f"${amount} Removed from {user}'s account."
        except Error as e:
            print(e)

    @staticmethod
    def open_account(name):
        """Creates an account for a user"""
        insert_query = f"INSERT INTO `accounts` (user, balance) VALUES ('{name}', '10.00')"

        try:
            with connect(
                    host=host,
                    user=user,
                    password=password,
                    database=database
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(insert_query)
                    connection.commit()
        except Error as e:
            print(e)

    @commands.command(aliases=['b', 'bal'])
    async def balance(self, ctx):
        """See how much money you have"""
        if not Bank.has_account(ctx.author.name):
            self.open_account(ctx.author.name)

        query = f"SELECT `balance` FROM `accounts` WHERE `user` = '{ctx.author.name}'"

        try:
            with connect(
                    host=host,
                    user=user,
                    password=password,
                    database=database
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    result = cursor.fetchall()[0][0]
                    connection.commit()
        except Error as e:
            print(e)
        await ctx.send(f"***{ctx.author.name} Account***\nBalance: ${result}")

    @commands.command()
    @commands.has_any_role("Administrator")
    async def add(self, ctx, amount):
        """Administrators can add money to an account"""
        Bank.add_money(ctx.author.name, amount)
        await ctx.send(f"Added ${amount} from {ctx.author.name}'s account.")

    @commands.command()
    @commands.has_any_role("Administrator")
    async def sub(self, ctx, amount):
        """Administrators can remove money from an account"""
        Bank.sub_money(ctx.author.name, amount)
        await ctx.send(f"Removed ${amount} from {ctx.author.name}'s account.")

    # @commands.command(description='A place to spend your money!',aliases=['s'])
    # async def shop(self,ctx):
    #     '''View commands to buy things'''
    #     pass

def setup(bot):
    bot.add_cog(Bank(bot))

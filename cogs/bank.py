import os
from discord.ext import commands
from mysql.connector import connect, Error
import logging

host = os.getenv()
user = os.getenv()
password = os.getenv()
database = os.getenv()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(name)s:%(asctime)s:%(levelname)s:%(message)s')
file_handler = logging.FileHandler('bot.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def query_db(query):
    try:
        with connect(
                host=host,
                user=user,
                password=password,
                database=database
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                logger.info(f"Query performed: {query}.")
                logger.info(f"Query results: {result}.")
                connection.commit()
                return result
    except Error as e:
        logger.warning(f"Error with mySQL query. {e}")
        print(e)


class Bank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def has_account(name):
        """Checks if the name is in DB"""
        query = f"SELECT `user` FROM `accounts` WHERE `user` = '{name}'"
        results = query_db(query)
        if results:
            return True
        else:
            return False

    @staticmethod
    def add_money(name, amount):
        """Adds money to an account"""
        if not Bank.has_account(name):
            Bank.open_account(name)

        add_query = f"UPDATE `accounts` SET `balance` = balance + {amount} WHERE `user` = '{name}'"
        query_db(add_query)
        return f"${amount} Added to {name}'s account."

    @staticmethod
    def sub_money(name, amount):
        """Subtracts money from an account"""
        if not Bank.has_account(name):
            Bank.open_account(name)

        sub_query = f"UPDATE `accounts` SET `balance` = balance - {amount} WHERE `user` = '{name}'"
        query_db(sub_query)
        return f"${amount} Removed from {user}'s account."

    @staticmethod
    def open_account(name):
        """Creates an account for a user"""
        insert_query = f"INSERT INTO `accounts` (user, balance) VALUES ('{name}', '10.00')"
        query_db(insert_query)

    @commands.command(aliases=['b', 'bal'])
    async def balance(self, ctx):
        """See how much money you have"""
        if not Bank.has_account(ctx.author.name):
            self.open_account(ctx.author.name)

        query = f"SELECT `balance` FROM `accounts` WHERE `user` = '{ctx.author.name}'"
        results = query_db(query)
        await ctx.send(f"***{ctx.author.name} Account***\nBalance: ${results[0][0]}")

    @commands.command()
    @commands.has_any_role("Administrator")
    async def add(self, ctx, amount):
        """Administrators can add money to an account"""
        Bank.add_money(ctx.author.name, amount)
        logger.info(f"User {ctx.author.name} has added ${amount} to their account.")
        await ctx.send(f"Added ${amount} from {ctx.author.name}'s account.")

    @commands.command()
    @commands.has_any_role("Administrator")
    async def sub(self, ctx, amount):
        """Administrators can remove money from an account"""
        Bank.sub_money(ctx.author.name, amount)
        logger.info(f"User {ctx.author.name} has removed ${amount} from their account.")
        await ctx.send(f"Removed ${amount} from {ctx.author.name}'s account.")

    # @commands.command(description='A place to spend your money!',aliases=['s'])
    # async def shop(self,ctx):
    #     '''View commands to buy things'''
    #     pass

def setup(bot):
    bot.add_cog(Bank(bot))

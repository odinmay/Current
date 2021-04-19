from discord.ext import commands
import discord


class Base_New_Cog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Base_New_Cog(bot))

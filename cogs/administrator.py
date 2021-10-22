from discord.ext import commands
from datetime import datetime
import discord
import asyncio
import math
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
file_handler = logging.FileHandler('bot.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class Administration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """Prints the bots ping in ms"""
        await ctx.send(f'Currents current ping is {round(self.bot.latency * 1000)}ms')

    @commands.command()
    @commands.has_permissions()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kicks target member"""
        await member.kick(reason=reason)
        ctx.send(f'{ctx.author} has kicked {member}')

    @commands.command()
    @commands.has_permissions()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Bans target member"""
        await member.ban(reason=reason)
        await ctx.send(f'{member.mention} has been banned.')

    @commands.command()
    @commands.has_permissions()
    async def unban(self, ctx, *, member):
        """Unbans target member"""
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'{ctx.author} Unbanned {user.mention}')
                return

    @commands.command()
    async def list_channels(self, ctx):
        """Pulls all of the guild channels and displays them in an Embed message"""
        # Create Embed object and set attrs
        embedMsg = discord.Embed(title=f"{ctx.guild} Channels", description="Channels", color=0x00C7FF)

        # Adds every channel as a field of the Embed object
        for channel in ctx.guild.channels:
            embedMsg.add_field(
                name=f"{channel}",
                value=f"Created at - {channel.created_at.strftime('%B %d, %Y : %I %M %p')}",
                inline=False
            )

        await ctx.send(embed=embedMsg)

    @commands.command()
    async def emojis(self, ctx):
        """Print the total emojis available to the Guild"""
        await ctx.send(f'{ctx.guild} has {len(ctx.guild.emojis)} emojis available!')

    @commands.command()
    async def server_birthday(self, ctx):
        """Prints the date the Guild was created at"""
        await ctx.send(f'{ctx.guild}\'s Birthday is : {ctx.guild.created_at.strftime("%B %d, %Y : %I %M %p")}')


    # Credit to Diggy. https://stackoverflow.com/questions/61786264/discord-py-send-long-messages
    @commands.command()
    async def members(self, ctx):
        """Prints all of the members on the server"""
        members = [str(m) for m in ctx.guild.members]
        per_page = 10  # 10 members per page
        pages = math.ceil(len(members) / per_page)
        cur_page = 1
        chunk = members[:per_page]
        linebreak = "\n"
        message = await ctx.send(f"Page {cur_page}/{pages}:\n{linebreak.join(chunk)}")
        await message.add_reaction("◀️")
        await message.add_reaction("▶️")
        active = True

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]
            # or you can use unicodes, respectively: "\u25c0" or "\u25b6"

        while active:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)

                if str(reaction.emoji) == "▶️" and cur_page != pages:
                    cur_page += 1
                    if cur_page != pages:
                        chunk = members[(cur_page - 1) * per_page:cur_page * per_page]
                    else:
                        chunk = members[(cur_page - 1) * per_page:]
                    await message.edit(content=f"Page {cur_page}/{pages}:\n{linebreak.join(chunk)}")
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "◀️" and cur_page > 1:
                    cur_page -= 1
                    chunk = members[(cur_page - 1) * per_page:cur_page * per_page]
                    await message.edit(content=f"Page {cur_page}/{pages}:\n{linebreak.join(chunk)}")
                    await message.remove_reaction(reaction, user)
            except asyncio.TimeoutError:
                await message.delete()
                active = False

    @commands.command()
    async def boosters(self, ctx):
        """
        Print the server boosters of the guild
        and how long they have been boosting it.
        """
        embedMsg = discord.Embed(title=f"{ctx.guild}'s Loyal Boosters!", description="Thank you!", color=0xFF00FF)

        for member in ctx.guild.premium_subscribers:
            embedMsg.add_field(name=f"{member.display_name}",
                               value=f"Boosting Since - {member.premium_since.strftime('%B %d, %Y')}.", inline=False)
        await ctx.send(embed=embedMsg)

    @commands.command()
    async def member_count(self, ctx):
        """Prints the # of members"""
        await ctx.send(f'There are {ctx.guild.member_count} members currently in {ctx.guild}')


def setup(bot):
    bot.add_cog(Administration(bot))

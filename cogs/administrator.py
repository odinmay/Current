from discord.ext import commands
from datetime import datetime
import discord



class Administration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Prints the bots ping in ms')
    async def ping(self, ctx):
        await ctx.send(f'Odinbots current ping is {round(self.bot.latency * 1000)}ms')

    @commands.command(name='clear')
    async def clear(self, ctx, amount=0):
        if ctx.author.guild_permissions.manage_messages:
            await ctx.channel.purge(limit=amount)
        else:
            await ctx.channel.purge(limit=1)
            await ctx.send(f'{ctx.author} does not have permission to delete messages.')

    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if ctx.author.guild_permissions.kick_members:
            await member.kick(reason=reason)
            ctx.send(f'{ctx.author} has kicked {member}')
        else:
            await ctx.send(f'{ctx.author} does not have permission to kick members.')

    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if ctx.author.guild_permissions.ban_members:
            await member.ban(reason=reason)
            await ctx.send(f'{member.mention} has been banned.')
        else:
            await ctx.send(f'{ctx.author} does not have permission to ban members.')

    @commands.command()
    async def add_role(self, ctx):
        await ctx.send(ctx.author.roles)

    @commands.command()
    async def unban(self, ctx, *, member):
        if ctx.author.guild_permissions.ban_members:
            banned_users = await ctx.guild.bans()
            member_name, member_discriminator = member.split('#')
            for ban_entry in banned_users:
                user = ban_entry.user
                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    await ctx.guild.unban(user)
                    await ctx.send(f'{ctx.author} Unbanned {user.mention}')
                    return
        else:
            await ctx.send(f'{ctx.author} does not have permission to unban members.')

    @commands.command()
    async def list_channels(self, ctx):
        """
        Pulls all of the guild channels and displays them in an Embed message
        """

        # Create Embed object and set attrs
        embedMsg = discord.Embed(title=f"{ctx.guild} Channels", description="Channels", color=0x00C7FF)

        # Adds every channel as a field of the Embed object
        for channel in ctx.guild.channels:
            embedMsg.add_field(name=f"{channel}", value=f"Created at - {channel.created_at}", inline=False)

        await ctx.send(embed=embedMsg)

    @commands.command()
    async def emojis(self, ctx):
        """
        Print the total emojis available to the Guild
        """
        await ctx.send(f'{ctx.guild} has {len(ctx.guild.emojis)} emojis available!')

    @commands.command()
    async def server_birthday(self, ctx):
        """
        Prints the date the Guild was created at
        """

        await ctx.send(f'{ctx.guild}\'s Birthday is : {ctx.guild.created_at}')

    @commands.command()
    async def backup_messages(self, ctx):
        all_messages = []
        for channel in ctx.guild.text_channels:
            print(f'Working on Channel: {channel}')
            messages = await channel.history(limit=150000).flatten()
            for message in messages:
                all_messages.append(f'Channel: {channel} - {message.author} : {message.content} | {message.created_at}')
        print('Opening File')

        with open(f'Message_backup_{datetime.today().strftime("%Y-%m-%d")}.txt', 'w') as file:
            for message in all_messages:
                file.write(message + '\n')


def setup(bot):
    bot.add_cog(Administration(bot))

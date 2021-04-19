from discord.ext import commands
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


def setup(bot):
    bot.add_cog(Administration(bot))

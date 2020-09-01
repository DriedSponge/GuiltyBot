import discord
import random
import index
import json
import datetime
from discord.ext import commands


class Status(commands.Cog, name='Status'):
    """Status"""

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.guild_only()
    async def status(self, ctx, status: int = 1, *, message: str = None):
        if ctx.author.id in index.Authors:
            try:
                with open('status.json') as fole:
                    midon = json.load(fole)
                oldstatid = int(midon['msgid'])
                print(oldstatid)
                oldstat = await ctx.message.channel.fetch_message(id=oldstatid)
                await oldstat.delete()
            except discord.NotFound:
                print('Message not found')
            color = 0x43B581
            title = ''
            if status == 1:
                color = 0x43B581
                title = 'Avaliable';
            if status == 2:
                color = 0xFAA61A
                title = 'Busy';
            if status == 3:
                color = 0xF04747
                title = 'Not Avaliable';
            embed = discord.Embed(color=color)
            embed.set_author(name="Guilty's Status", icon_url=self.client.user.avatar_url)
            embed.add_field(name='Status', value=title, inline=False)
            embed.timestamp = datetime.datetime.utcnow()
            if message is not None:
                embed.add_field(name='Message', value=message, inline=False)
            await ctx.message.delete()
            response = await ctx.channel.send(embed=embed)
            NewStatus = {
                "statusid": status,
                "statusmsg": message,
                "msgid": response.id
            }
            with open('status.json', 'w') as json_file:
                index.json.dump(NewStatus, json_file)
            await index.UpdateStatus()

    @status.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.message.delete()
            respose = await ctx.send(f'{ctx.author.mention} Missing required argument')
            await respose.delete(delay=5)
        if isinstance(error, commands.BadArgument):
            await ctx.message.delete()
            respose = await ctx.send(f'{ctx.author.mention} Invalid arguemnt')
            await respose.delete(delay=5)


def setup(client):
    client.add_cog(Status(client))

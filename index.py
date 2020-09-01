import json
import discord
import random
import datetime
import os
from discord.ext import commands

with open('botinfo.json') as file:
    data = json.load(file)

client = commands.Bot(command_prefix=data['prefix'])



async def UpdateStatus():
    with open('status.json') as status:
        stat = json.load(status)
    CurStat = stat['statusid']
    if CurStat == 1:
        showstatus = discord.Status.online
    if CurStat == 2:
        showstatus = discord.Status.idle
    if CurStat == 3:
        showstatus = discord.Status.do_not_disturb

    await client.change_presence(status=showstatus, activity=discord.Game(name=stat['statusmsg']))


@client.event
async def on_ready():
    print('Bot is ready')
    await UpdateStatus()


Authors = [186920808076148736, 283710670409826304]


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.NoPrivateMessage):
        await ctx.send(f'{ctx.author.mention} Please use this command in the server')
    if isinstance(error, commands.CommandNotFound):
        response = await ctx.send(f'{ctx.author.mention} That command does not exist')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.mention} You do not have permission to use that command')
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send(f'{ctx.author.mention} I do not have permission to do this')
    if isinstance(error, commands.NotOwner):
        await ctx.send(f'{ctx.author.mention} You must be the owner of the bot to perform this action')


for filename in os.listdir('./commands'):
    if filename.endswith('.py'):
        client.load_extension(f'commands.{filename[:-3]}')
        print(f'{filename} loaded!')

client.run(data['token'])

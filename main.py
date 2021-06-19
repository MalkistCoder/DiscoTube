import discord
from discord.ext import commands
from webserver import keep_alive
import random as rng
import os
import asyncio


client = commands.Bot(command_prefix='ayo ')


#when the bot is ready
@client.event
async def on_ready():
    print('bot is ready to roll as {0.user}'.format(client))


#says ping of the user
@client.command()
async def ping(ctx):
    await ctx.send('Pong! your ping is {}ms'.format(round(client.latency * 1000)))



#have no perms idiot
@client.event
async def on_command_error(ctx,error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Ayo bro you know a Thing Called **PERMS**??")





my_secret = os.environ['MY_BOT_TOKEN']

extensions = [
  'cogs.economy',
  'cogs.fun',
  'cogs.moderation'
]





if __name__ == '__main__':
    for extension in extensions:
        client.load_extension(extension)

keep_alive()
client.run(my_secret)

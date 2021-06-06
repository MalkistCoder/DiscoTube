import discord
from discord.ext import commands
import json
from webserver import keep_alive
import random as rng
import os


client = commands.Bot(command_prefix='ayo ')


#when the bot is ready
@client.event
async def on_ready():
    print('bot is ready to roll as {0.user}'.format(client))




#says ping of the user
@client.command()
async def ping(ctx):
    await ctx.send('Pong! your ping is {}ms'.format(round(client.latency * 1000)))


#random numbers!
@client.command(name='random')
async def random(ctx, a:int=1, b:int=1000):
    await ctx.reply('DiscoTube Rolls a Random Number . . . . ' +str(rng.randint(int(a), int(b))), mention_author=False)


#random numbers!
@client.command(name='lucky')
async def random(ctx, a:int=1, b:int=1000):
    await ctx.reply('Your Lucky Number Is. . . . ' +str(rng.randint(int(a), int(b))), mention_author=False)



#8ball
@client.command(name='8ball')
async def eightball(ctx,*,q:str=None):
    if (len(q.split(' ')) >= 3 or len(q) >= 5) and q != None: # For example: "You like jazz?"
        eightball_outcomes = ['Yes!','Nope.','<a:NO:850318483261620224>']
        outcome = str(rng.choice(eightball_outcomes))
        await ctx.reply(outcome, mention_author=False)
    else:
        await ctx.send('Invalid Question or some error may have occured..')



#bot online        
@client.command(name='on')
async def online(ctx):
  await ctx.reply('Hey Bro Chill <a:Chill:850283396751294465> , Im Online ', mention_author=False)



#wassup
@client.command(name='sup')
async def wassup(ctx):
  await ctx.reply(f'heyyyy brooooo WasSup')










my_secret = os.environ['MY_BOT_TOKEN']

extensions = [
  'cogs.economy'
]

if __name__ == '__main__':
    for extension in extensions:
        client.load_extension(extension)

keep_alive()
client.run(my_secret)

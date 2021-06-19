from discord.ext import commands
import discord
import json,os
import random as rng
from PIL import Image,ImageFont,ImageDraw
from io import BytesIO

class Fun(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    #random numbers!
    @commands.command(name='random')
    async def random(self,ctx, a:int=1, b:int=1000):
        await ctx.reply('DiscoTube Rolls a Random Number . . . . ' +str(rng.randint(int(a), int(b))), mention_author=False)



    #8ball
    @commands.command(name='8ball')
    async def eightball(self, ctx,*,q:str=None):
        if (len(q.split(' ')) >= 3 or len(q) >= 5) and q != None: # For example: "You like jazz?"
            eightball_outcomes = ['Yes!','<a:NO:850318483261620224>','<:no:851112289540505601>']
            outcome = str(rng.choice(eightball_outcomes))
            await ctx.reply(outcome, mention_author=False)
        else:
            await ctx.send('Invalid Question or some error may have occured..')



    #bot online        
    @commands.command(name='on')
    async def online(self,ctx):
        await ctx.reply('Hey Bro Chill <a:Chill:850283396751294465> , Im Online ')



    #wassup
    @commands.command(name='sup')
    async def wassup(self,ctx):

        await ctx.reply(f'hey Broooooo WHAT IS UP?')



     
    #stonks image generation
    @commands.command(aliases=['st','sto','stocks',])
    async def stonkaaa(self,ctx):

	    stonk = Image.open("stonksmage.jpg")

	    draw = ImageDraw.Draw(stonk)
	    font = ImageFont.truetype("calibrib.ttf", 11)

	    price = "$250 P/Dsc"

	    status = "Production > Demand"

	    draw.text((211,64), price, (255, 255, 255), font=font)
	    draw.text((18,97), status, (255, 255, 255), font=font)
	    stonk.save("stonkletts.jpg")

	    await ctx.send(file = discord.File("stonkletts.jpg"))



def setup(bot):
    bot.add_cog(Fun(bot))
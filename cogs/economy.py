from discord.ext import commands, tasks
import discord
import random
import json



#adds accounts for user
async def add_account(memberid: int):
    with open('economy.json','r') as f:
        banks = json.load(f)
    if not memberid in banks['banks']:
        banks['banks'][str(memberid)] = {}
        banks['banks'][str(memberid)]['subs'] = 0
        banks['banks'][str(memberid)]['money'] = 1000
        banks['banks'][str(memberid)]['inventory'] = {}
        with open('economy.json','w') as f:
            json.dump(banks,f,indent=4)










# idk what it does
class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot








    #balance command
    @commands.command()
    async def bal(self, ctx, member:discord.Member=None):
        if member == None:
            member = ctx.message.author
        
        await add_account(member.id)

        with open('economy.json','r') as f:
            banks = json.load(f)

        embed = discord.Embed(title=f'{member.display_name}\'s Account',color=0xff0000)
        embed.add_field(name='Subscribers',value=str(banks['banks'][str(member.id)]['subs']),inline=False)
        embed.add_field(name='Money',value=str(banks['banks'][str(member.id)]['money']),inline=False)

        await ctx.reply(embed=embed)
    






    #user uploads videos and gets some sweet revenue.. . .
    @commands.command(aliases=['vid','yt','ytvid','youtube','youtubevideo','youtubevid','film','youtubefilm','ytfilm'])
    async def video(self,ctx):
        with open('economy.json','r') as f:
            banks = json.load(f)
        
        vid_chs = [random.choice(banks['trends']) for i in range(4)]
        await ctx.send(embed=discord.Embed(title='What Type of Video do You want To Make?',description=f'{vid_chs[0]}\n{vid_chs[1]}\n{vid_chs[2]}\n{vid_chs[3]}'))

        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author
        
        await self.bot.wait_for('message',check=check,timeout=10.0)
        last_message = (ctx.channel.last_message).lower()

        subs = banks['banks'][str(ctx.author.id)]['subs']

        views = round((random.randint(100,200)/100)*(7.5+subs) * random.randint(85,115)/100)
        subs_gained = round(views // 4)
        if subs >= 1000:
            ad_revenue = round((subs_gained + views) // (166 + 2/3))
        else:
            ad_revenue = 0

        banks['banks'][str(ctx.author.id)]['subs'] += subs_gained

        await ctx.reply(f'You chose to do a {last_message.clean_content} video! You got {views} views and gained {subs_gained}, You also got ${ad_revenue} from the ads.')

        with open('economy.json','w') as f:
            json.dump(banks,f,indent=4)




def setup(bot):
    bot.add_cog(Economy(bot))
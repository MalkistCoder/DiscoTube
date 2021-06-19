from discord.ext import commands, tasks
from discord.ext.commands.cooldowns import BucketType
from math import floor,sin,cos,tan,sqrt
from colorama import Fore, Fore, Style
from colorama import init as clrinit
import datetime
import discord
import random
import sys,os
import json


clrinit(autoreset=True)


#adds accounts for user
async def add_account(memberid: int):
    with open('economy.json', 'r') as f:
        banks = json.load(f)
    if str(memberid) in banks['banks']:
        pass
    else:
        banks['banks'][str(memberid)] = {}
        banks['banks'][str(memberid)]['subs'] = 0
        banks['banks'][str(memberid)]['money'] = 1000
        banks['banks'][str(memberid)]['inventory'] = {}
        banks['banks'][str(memberid)]['has_registered_discoin_account'] = False,
        banks['banks'][str(memberid)]['discoin_bal'] = 0 
        with open('economy.json', 'w') as f:
            json.dump(banks, f, indent=4)




@tasks.loop(seconds=60)
async def discoin_price():
    with open('economy-dc.json','r') as f:
        dcoin = json.load(f)
        
    if dcoin['exists'] == True:
        dcoin['time_it_existed'] += 1

        #main stoof

        time_up = dcoin['time_it_existed']
        price_b4 = dcoin['price']
        buys,sells = dcoin['buys_this_minute'],dcoin['sells_this_minute']
        price_now = None

        if dcoin['buys_this_minute'] > dcoin['sells_this_minute']: # More buys
            dcoin['price'] += round(dcoin['buys_this_minute']/1.5)
            price_now = price_b4 + round(dcoin['buys_this_minute']/1.5)

            print(f'Minute {Fore.CYAN}{time_up}{Style.RESET_ALL}: {Fore.GREEN}{buys} buys{Style.RESET_ALL} {Style.DIM}&{Style.RESET_ALL} {Fore.RED}{sells} sells{Style.RESET_ALL}, Price: {Fore.YELLOW}{price_now}{Style.RESET_ALL}, used to be {Fore.YELLOW}{price_b4}{Style.RESET_ALL}')

        elif dcoin['buys_this_minute'] < dcoin['sells_this_minute']: # More sells
            dcoin['price'] -= round(dcoin['sells_this_minute']/1.5)
            price_now = price_b4 + round(dcoin['buys_this_minute']/1.5)

            print(f'Minute {Fore.CYAN}{time_up}{Style.RESET_ALL}: {Fore.GREEN}{buys} buys{Style.RESET_ALL} {Style.DIM}&{Style.RESET_ALL} {Fore.RED}{sells} sells{Style.RESET_ALL}, Price: {Fore.YELLOW}{price_now}{Style.RESET_ALL}, used to be {Fore.YELLOW}{price_b4}{Style.RESET_ALL}')

        else: # Same price, nothing changes.
            price_now = price_b4 + round(dcoin['buys_this_minute']/1.5)
            print(f'Minute {Fore.CYAN}{time_up}{Style.RESET_ALL}: {Fore.GREEN}{buys} buys{Style.RESET_ALL} {Style.DIM}&{Style.RESET_ALL} {Fore.RED}{sells} sells{Style.RESET_ALL}, Price: {Fore.YELLOW}{price_now}{Style.RESET_ALL}, used to be {Fore.YELLOW}{price_b4}{Style.RESET_ALL}')
            
        dcoin['buys_this_minute'], dcoin['sells_this_minute'] = 0, 0


        with open('economy-dc.json','w') as f:
            json.dump(dcoin,f,indent=4)
    else:
        print(f'{Style.DIM}DisCoin is off.')
    

# idk what it does
# It defines the cog lol
class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot





    #balance command
    @commands.command(aliases=['balance','openaccount','statistics','stats'])
    async def bal(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.message.author

        await add_account(member.id)

        with open('economy.json', 'r') as f:
            banks = json.load(f)

        embed = discord.Embed(title=f'{member.display_name}\'s Account Stats',
                              color=0xff0000)
        embed.add_field(name='Subscribers :',
                        value=banks['banks'][str(member.id)]['subs'],
                        inline=False)
        embed.add_field(name='Money :',
                        value='$'+str(banks['banks'][str(member.id)]['money']),
                        inline=False)
        embed.add_field(name='DisCoins :',value=f'<:discoin:855657870531624990>'+str(banks['banks'][str(member.id)]['discoin_bal']))

        if banks['banks'][str(member.id)]['subs'] > 1e12:
            embed.set_footer('OMG GUYS ITS PEWDIEPIE 2')
        elif 1e9 < banks['banks'][str(member.id)]['subs'] <= 1e12:
            embed.set_footer('OMG GUYS ITS PEWDIEPIE')
        elif 1e6 < banks['banks'][str(member.id)]['subs'] <= 1e9:
            embed.set_footer(f'Oh, you don\'t know who {member.mention} is? \*intense distorted voice\* **I**T***S*** **J**U***S***T **S**O***M***E **D**U***D***E**!**')
        elif 1e5 < banks['banks'][str(member.id)]['subs'] <= 1e6:
            embed.set_footer('😏')
        elif 1e3 < banks['banks'][str(member.id)]['subs'] <= 1e5:
            embed.set_footer(f'Not, bad, but {member.mention} has to grind a bit more')
        elif banks['banks'][str(member.id)]['subs'] <= 1e3:
            embed.set_footer(f'He\'s trying to find a way to break the youtube algorithm')
        

        await ctx.reply(embed=embed)





    #user uploads videos and gets some sweet revenue.. . .
    @commands.command(aliases=[
        'vid', 'yt', 'ytvid', 'youtube', 'youtubevideo', 'youtubevid', 'film',
        'youtubefilm', 'ytfilm'
    ])
    @commands.cooldown(1,30,BucketType.member)
    async def video(self, ctx):
        with open('economy.json', 'r') as f:
            banks = json.load(f)
       




       
        #Video Choices and the complex system
        vid_chs = [random.choice(list(banks['trends'].keys())) for i in range(4)]
        embed = discord.Embed(
            title='What Type of Video do You want To Make?',
            description=
            f'1. {vid_chs[0]}\n2. {vid_chs[1]}\n3. {vid_chs[2]}\n4. {vid_chs[3]}')
        embed.set_footer(text='Send a message that contains the numberr next to the topic that you want!')
        await ctx.send(embed=embed)

        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author

        await self.bot.wait_for('message', check=check, timeout=10.0)
        last_message = int(ctx.channel.last_message.clean_content)

        chance_of_success = banks['trends'][vid_chs[last_message-1]]
        did_succeed = random.uniform(0,1) < chance_of_success


        subs = banks['banks'][str(ctx.author.id)]['subs']

        


        #Give revenue System
        if did_succeed:
            views = round((random.randint(100, 200) / 100) * (7.5 + subs) * random.randint(85, 115) / 100)
            subs_gained = round(views // 4)
            if subs >= 1000:
                ad_revenue = round((subs_gained + views) // (166 + 2 / 3))
            else:
                ad_revenue = 0

            banks['banks'][str(ctx.author.id)]['subs'] += subs_gained
            banks['banks'][str(ctx.author.id)]['money'] += ad_revenue
        


            #Sends the fin msg
            await ctx.reply(
                f'You chose to do a {vid_chs[last_message-1]} video! You got {views} views and gained {subs_gained}, You also got ${ad_revenue} from the ads.', mention_author=False
            )
            if random.uniform(0,1) < 0.05:
                sponsor = random.choice(banks['sponsors'])
                xtra_cash = random.randint(100,200)
                await ctx.send(f':tada:**!BONUS!**:tada:\n{sponsor} sponsored your video! You got an extra ${xtra_cash} from them.')
        else:
            unsubs = round((random.randint(2,10)/100) * subs)
            banks['banks'][str(ctx.author.id)]['subs'] -= unsubs

            if unsubs == abs(unsubs):
                verb_add_or_subtract_subscribers = 'literally pooped out' # If you lose subs
            else:
                verb_add_or_subtract_subscribers = 'didn\'t really earn those' # If you Gain subs

            await ctx.reply(
                f'You chose to do a {vid_chs[last_message-1]} video! Your video didn\'t do quite well, so you {verb_add_or_subtract_subscribers} {abs(unsubs)} subscribers. You didn\'t get any ad revenue from the ads. . . . Sad Bro.')




        
        # Saves data, might not work sometimes if 2 ppl do at same time
        with open('economy.json', 'w') as f:
            json.dump(banks, f, indent=4)
    

    #Demotes users, kind of raiding, but opposite
    @commands.command(aliases=['downgrade','demoot','roast'])
    @commands.cooldown(1,120,BucketType.member)
    async def cancel(self,ctx,member:discord.Member=None):
        with open('economy.json','r') as f:
            banks = json.load(f)
        if member == None:
            await ctx.reply('Do you want to cancel nobody? Well, you can\'t show him naked because he has no body.')
            
        else:
            if str(member.id) not in banks['banks']:
                await ctx.reply('He hasn\'t made an account yet, so yeah . . .')
            else:
                if random.randint(1,2) == 1:
                    lost_subs = round((random.randint(4,20)/100) * banks['banks'][str(member.id)]['subs'])
                    gained_subs = round(lost_subs / 7.5)
                    banks['banks'][str(member.id)]['subs'] -= lost_subs
                    await ctx.reply(f'You made a really good roast on him and that made him lose {lost_subs}. Some of those {lost_subs} subscribed to you. So you also gained {gained_subs} subs, happy now bro?')

                    banks['banks'][str(member.id)]['subs'] -= lost_subs
                    banks['banks'][str(ctx.author.id)]['subs'] += gained_subs
                else:
                    lost_subs = round((random.randint(4,20)/100) * banks['banks'][str(ctx.author.id)]['subs'])
                    await ctx.reply(f'Your roast didn\'t really work well, so people started **_hating_** you and you actually lost subs. You lost {lost_subs} subscribers.')
                    banks['banks'][str(ctx.author.id)]['subs'] -= lost_subs
        
                with open('economy.json','w') as f:
                    json.dump(banks,f,indent=4)
    
    
    @commands.cooldown(1,100,BucketType.guild)
    @commands.command(name='discoinaccount',aliases=['discoina','discaccount','disca','dcoinaccount','dcoina','dcaccount','dca'])
    async def _discoin(self,ctx):
        with open('economy.json','r') as f:
            banks = json.load(f)
        if not banks['banks'][str(ctx.author.id)]['has_registered_discoin_account']:
            banks['banks'][str(ctx.author.id)]['has_registered_discoin_account'] = True
            await ctx.reply('Well done! You have registered a DisCoin account. Good luck!')
        with open('economy-dc.json','w') as f:
            json.dump(banks,f,indent=4)
    
    @commands.command()
    async def buydiscoin(self,ctx,amt:int=1):
        with open('economy.json') as f:
            banks = json.load(f)
        with open('economy-dc.json') as f:
            dcoin = json.load(f)
        
    
        

    #@commands.command()
    #async def stonk(self,ctx):
	#    embedio = discord.Embed(
    #        title="This Hour's Stonks !", 
    #        color=0xeb5534
    #    )
    #    embedio.add_field(name="Price = ", value="$250 P/Dsc")
    #    embedio.add_field(name="Status = ", value="Production > Demand")		
    #await ctx.reply(embed=embedio)


def setup(bot):
    bot.add_cog(Economy(bot))
    discoin_price.start()

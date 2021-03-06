from discord.ext import commands,tasks
import asyncio
import discord
import json,os


class Moderation(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command(aliases=['clear','purge','delete'])
    @commands.has_permissions(manage_messages=True)
    async def clean(self, ctx, limit: int):
            await ctx.channel.purge(limit=limit+1)
            botmessage = (f'{limit} messages cleared by {ctx.message.author.mention}')
            massage = await ctx.send(botmessage)
            await asyncio.sleep(2)
            await massage.delete()
    
    @commands.command(name='ban',aliases=['ayodudebyebye','banananananana'])
    @commands.has_permissions(ban_members=True)
    async def ban_c(self,ctx,member:discord.Member=None,*,reason='being cringe'):
        if member == None:
            await ctx.send('You can\'t ban no-one, he\'s busy protesting about ones.')
        else:
            await ctx.send('Are you sure you want to ban this member?\nSay `yes` in less than 15 seconds.')
            global_ctx = ctx
            def check(self,ctx):
                return ctx.author == global_ctx.author and ctx.channel == global_ctx.channel
            await self.bot.wait_for('message',check=check,timeout=15)
            await ctx.send(f'{member.mention} was banned. Good riddance!')
            await ctx.guild.ban(member,reason=f'Banned by {ctx.author.display_name} for {reason}')

    #have no perms idiot
    @commands.Cog.listener('on_command_error')
    async def on_command_error(self,ctx,error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Ayo bro you know a Thing Called **PERMS**??")
        elif isinstance(error,commands.CommandOnCooldown):
            embed = discord.Embed(
                title='Stop spamming commands!',
                description=f'{ctx.author.mention}, wait about {round(error.retry_after)} before you try using the {ctx.command.name} command again.',
                color=0x663399
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send(str(type(error))+'\n'+str(error))
            raise error



def setup(bot):
    bot.add_cog(Moderation(bot))
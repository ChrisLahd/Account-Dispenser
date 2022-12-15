import discord
import time
import datetime
import os
from discord.ext import commands

prefix = open("prefix.txt", "r").read()

class General(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.commands = {
            "Help": "Shows this command",
            "Ping": "Shows bot latency to the discord servers",
            "Account": f"Shows help for account commands **Use {prefix}help account**",
            "Admin": "Displays admin menu"
        }

        self.accountmenucommands = {
            "Accounts": "Shows our current account types aswell as stock",
            "Generate": "Generates you an account of the type you input"
        }
        
        self.CommandKeyList = []
        self.CommandValList = []

        for i in range(len(self.commands)):
            self.CommandKeyList.append(list(self.commands)[i])
            self.CommandValList.append(list(self.commands.values())[i])

        self.AccCmdKeyList = []
        self.AccCmdValList = []

        for i in range(len(self.accountmenucommands)):
            self.AccCmdKeyList.append(list(self.accountmenucommands)[i])
            self.AccCmdValList.append(list(self.accountmenucommands.values())[i])


    @commands.Cog.listener()
    async def on_ready(self):
        print("General cog loaded.")
        await self.bot.change_presence(status=discord.Status.idle, activity=discord.Game(name=f"{prefix}help"), )

    @commands.group(name="help", invoke_without_command=True)
    async def help(self, ctx):

        isInline = False

        embed = discord.Embed(title="Account Dispenser", description="How to use the bot", colour=0xe67e22, timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1049934047444484156/1052804133641539584/Illustration.png")
        
        for i in range(len(self.CommandKeyList)):
       
            if i >= 4:
                isInline = True
       
            embed.add_field(name=f"{self.CommandKeyList[i]}", value=f"{self.CommandValList[i]}", inline=isInline)
       
        await ctx.send(embed = embed)
            
    @help.command(aliases=["Account"])
    async def account(self, ctx):
        
        isInline = False

        embed = discord.Embed(title="Account Menu", description="Account commands to help you with using the unique features of the bot.", color=0xe67e22, timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1049934047444484156/1052804133641539584/Illustration.png")

        for i in range(len(self.AccCmdKeyList)):
       
            if i >= 4:
                isInline = True
       
            embed.add_field(name=f"{self.AccCmdKeyList[i]}", value=f"{self.AccCmdValList[i]}", inline=isInline)
       
        await ctx.send(embed = embed)

    @commands.command(aliases=["Ping"])
    async def ping(self, ctx):
        
        before = time.monotonic()
        message = await ctx.send("Pong!")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"Pong!  `{int(ping)}ms`")


async def setup(bot):
    await bot.add_cog(General(bot))
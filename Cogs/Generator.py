import discord
from discord.ext import commands
import os
import datetime

prefix = open("prefix.txt", "r").read()

class Generator(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.accountTypes = []
        self.accountTypeStock = []

        self.canuse = False

        for i in os.listdir("./Accounts"):
            if i.endswith(".txt"):
                self.accountTypes.append(i[:-4])

        for i in range(len(self.accountTypes)):
            x = len(open(f"./Accounts/{self.accountTypes[i]}.txt", "r").readlines())
            self.accountTypeStock.append(f"{x}")
    
    async def updateAccounts(self):
        self.accountTypes.clear()
        self.accountTypeStock.clear()

        for i in os.listdir("./Accounts"):
            if i.endswith(".txt"):
                self.accountTypes.append(i[:-4])

        for i in range(len(self.accountTypes)):
            x = len(open(f"./Accounts/{self.accountTypes[i]}.txt", "r").readlines())
            self.accountTypeStock.append(f"{x}")

    async def IDCheck(self, uid):
        idFile = open("ClientIDs.txt", "r").readlines()

        for line in idFile:
            line = line.split("\n")
            line = line[0].split("=")
            if line[0] != str(uid):
                self.canuse = False
            else:
                self.canuse = True
                return

    @commands.Cog.listener()
    async def on_ready(self):
        print("Generator cog loaded.")

    @commands.command(aliases=["Accounts"])
    async def accounts(self, ctx):
        isInline = False

        await self.updateAccounts()
        embed = discord.Embed(title="Accounts", description="Our current accounts aswell as the stock", colour=0xe67e22, timestamp=datetime.datetime.utcnow())

        for i in range(len(self.accountTypes)):
            if i >= 4:
                isInline = True
            else:
                isInline = False

            embed.add_field(name=f"Account Type: {self.accountTypes[i]}", value=f"Stock: {self.accountTypeStock[i]}", inline=isInline)

        await ctx.send(embed = embed)

    @commands.command(aliases=["Generate", "gen"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def generate(self, ctx, *accountType: str):
        iloopcount = -1

        await self.IDCheck(ctx.author.id)

        if self.canuse == False:
            await ctx.send("You do not have permission to use this feature.")
            return

        if len(list(accountType)) == 0 or str(list(accountType)[0].lower()) not in str(self.accountTypes).lower():
            embed = discord.Embed(title="Account Generation", description=f"Use {prefix}generate [Account type] to generate an account. We reccommend you use this in your DM's", color=0xe67e22, timestamp=datetime.datetime.utcnow())
            await ctx.send(embed = embed)
            Generator.generate.reset_cooldown(ctx)
        
        else:

            accountType = str(list(accountType)[0])

            for i in self.accountTypes:
                iloopcount += 1

                if str(i).lower() == accountType.lower():
                    Accounts = open(f"./Accounts/{self.accountTypes[iloopcount]}.txt", "r").readlines()
                    AccountsWrite = open(f"./Accounts/{self.accountTypes[iloopcount]}.txt", "w")
                    
                    if str(Accounts) == "[]":
                        await ctx.send(f"Sorry, our {accountType} accounts are out of stock.")
                        Generator.generate.reset_cooldown(ctx)
                        break

                    lineloopcount = 0
                    AccountToSend = Accounts[0]
                    
                    for line in Accounts:
                        lineloopcount += 1
                        
                        lineCount = len(Accounts)
                        line = line.strip("\n")
                        
                        if lineloopcount == lineCount:
                            NewLine = ""
                        else:
                            NewLine = "\n"

                        if line != AccountToSend.strip("\n"):
                            AccountsWrite.write(f"{line}{NewLine}")

        await ctx.send(f"```groovy\n{AccountToSend}```")

    @generate.error
    async def generate_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"You are on cooldown! Try again in {error.retry_after:.0f}s") 

async def setup(bot):
    await bot.add_cog(Generator(bot))
import discord
from discord.ext import commands
import os
import datetime
import asyncio

prefix = open("prefix.txt", "r").read()

class Generator(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.accountTypesFree = []
        self.accountTypeStockFree = []
        self.accountTypes = []
        self.accountTypeStock = []
        self.allAccTypes = []
        self.canuse = False
        self.canuseFree = True


    @commands.Cog.listener()
    async def on_ready(self):
        print("Generator cog loaded.")
        await self.updateAccountsDaemon()

    async def updateAccounts(self) -> None:
        self.accountTypesFree.clear()
        self.accountTypeStockFree.clear()
        self.accountTypes.clear()
        self.accountTypeStock.clear()
        self.allAccTypes.clear()

        for i in os.listdir("./AccountsFree"):
            if i.endswith("free.txt"):
                self.accountTypesFree.append(i[:-4])
                self.allAccTypes.append(i[:-4])

        for i in range(len(self.accountTypesFree)):
            x = len(open(f"./AccountsFree/{self.accountTypesFree[i]}.txt", "r").readlines())
            self.accountTypeStockFree.append(f"{x}")

        for i in os.listdir("./Accounts"):
            if i.endswith(".txt"):
                self.accountTypes.append(i[:-4])
                self.allAccTypes.append(i[:-4])

        for i in range(len(self.accountTypes)):
            x = len(open(f"./Accounts/{self.accountTypes[i]}.txt", "r").readlines())
            self.accountTypeStock.append(f"{x}")

    async def updateAccountsDaemon(self):
        await self.updateAccounts()
        await asyncio.sleep(1)
        await self.updateAccountsDaemon()
            

    async def IDCheck(self, uid) -> None:
        idFile = open("ClientIDs.txt", "r").readlines()

        for line in idFile:
            line = line.split("\n")
            line = line[0].split("=")
            if line[0] != str(uid):
                self.canuse = False
            else:
                self.canuse = True
                return

    @commands.command(aliases=["Accounts", "accs"])
    async def accounts(self, ctx):
        isInline = False

        await self.IDCheck(ctx.author.id)

        embed = discord.Embed(title="Accounts", description="Our current accounts aswell as the stock", colour=0xe67e22, timestamp=datetime.datetime.utcnow())

        if self.canuse:
            for i in range(len(self.accountTypes)):
                if i >= 4:
                    isInline = True

                embed.add_field(name=f"Account Type: {self.accountTypes[i]}", value=f"Stock: {self.accountTypeStock[i]}", inline=isInline)


        for i in range(len(self.accountTypesFree)):
            if i >= 4:
                isInline = True

            embed.add_field(name=f"Account Type: {self.accountTypesFree[i]}", value=f"Stock: {self.accountTypeStockFree[i]}", inline=isInline)

        await ctx.send(embed = embed)

    @commands.command(aliases=["Generate", "gen"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def generate(self, ctx, *accountType: str):
        iloopcount = -1

        print(self.allAccTypes)
        await self.IDCheck(ctx.author.id)
        if len(list(accountType)) == 0:
            embed = discord.Embed(title="Account Generation", description=f"Use {prefix}generate [Account type] to generate an account. We reccommend you use this in your DM's", color=0xe67e22, timestamp=datetime.datetime.utcnow())
            await ctx.send(embed = embed)
            Generator.generate.reset_cooldown(ctx)

        if self.canuse == False:
            await ctx.send("You do not have permission to use this feature.")
            return

        else:

            accountType = str(list(accountType)[0])
            
            if str(accountType).lower() in str(self.accountTypes).lower():
                AccToDispense = self.accountTypes
                path = "./Accounts/"
            else:
                AccToDispense = self.accountTypesFree
                path = "./AccountsFree/"

            for i in AccToDispense:
                iloopcount += 1

                if str(i).lower() == accountType.lower():
                    Accounts = open(f"{path}{AccToDispense[iloopcount]}.txt", "r").readlines()
                    AccountsWrite = open(f"{path}{AccToDispense[iloopcount]}.txt", "w")
                    
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
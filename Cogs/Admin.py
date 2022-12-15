from discord.ext import commands
import discord
import datetime
import os

class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.canuse = False
        self.admincommands = {
            "addUser": "Adds a user to the whitelist allowing them to use the bot",
            "removeUser": "Removes a users access to the bot",
            "addAdmin": "Makes users Admins (Use this carefully)",
            "removeAdmin": "Removes users from being Admins"
        }

        self.AdmCommandKeyList = []
        self.AdmCommandValList = []

        for i in range(len(self.admincommands)):
            self.AdmCommandKeyList.append(list(self.admincommands)[i])
            self.AdmCommandValList.append(list(self.admincommands.values())[i])

        self.ogFile = []
        self.stockFile = []
            
    @commands.Cog.listener()
    async def on_ready(self):
        print("Admin cog loaded.")

    async def IDCheck(self, uid):
        idFile = open("AdminIDs.txt", "r").readlines()

        for line in idFile:
            line = line.split("\n")
            if line[0] != str(uid):
                self.canuse = False
            else:
                self.canuse = True
                return

    @commands.command(aliases=["admin"])
    async def Admin(self, ctx):

        isInline = False

        await self.IDCheck(ctx.author.id)

        if self.canuse == False:
            await ctx.send("You do not have permission to use this feature.")
            return
        else:
        
            embed = discord.Embed(title="Admin Menu", description="Admin commands to help you manage the bot", color=0xe67e22, timestamp=datetime.datetime.utcnow())

            for i in range(len(self.AdmCommandKeyList)):
            
                if i >= 4:
                    isInline = True

                embed.add_field(name=f"{self.AdmCommandKeyList[i]}", value=f"{self.AdmCommandValList[i]}", inline=isInline)

            await ctx.send(embed = embed)

    @commands.command()
    async def restock(self, ctx, file: discord.Attachment):
        if file.content_type != "text/plain; charset=utf-8":
            await ctx.send("Incorrect file type.")
            return

        await discord.Attachment.save(file, f"Accounts/{file.filename}")

        newAccs = len(open(f"Accounts/{file.filename}", "r").readlines())

        await ctx.send(f"Restocked {file.filename[:-4]} with {newAccs} accounts")
    
async def setup(bot):
    await bot.add_cog(Admin(bot))
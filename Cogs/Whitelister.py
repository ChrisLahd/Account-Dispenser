from discord.ext import commands
import discord
import datetime

prefix = open("prefix.txt", "r").read()

class Whitelister(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.ids = []
        self.canuse = False

    @commands.Cog.listener()
    async def on_ready(self):
        print("Whitelister cog loaded.")

    async def IDCheck(self, uid):
        idFile = open("AdminIDs.txt", "r").readlines()

        for line in idFile:
            line = line.split("\n")
            if line[0] != str(uid):
                self.canuse = False
            else:
                self.canuse = True
                return

    @commands.command()
    async def addUser(self, ctx, *cid):
        await self.IDCheck(ctx.author.id)

        if self.canuse == False:
            await ctx.send("You do not have permission to use this feature.")
            return

        if len(list(cid)) == 0:
            embed = discord.Embed(title="Adding Users", description=f"Using the addUsers command is as simple as inputting the user's Discord ID.\n{prefix}addUser [UserID]", colour=0xe67e22, timestamp=datetime.datetime.utcnow())
            embed.set_image(url="https://cdn.discordapp.com/attachments/1052059625752629258/1052720946034782268/image.png")
            await ctx.send(embed = embed)
            return

        cidFileCheck = open("ClientIDs.txt", "r").readlines()

        for line in cidFileCheck:
            line = line.strip("\n")
            if line == cid:
                await ctx.send(f"User ID {cid} already whitelited.")
                return
            else:
                pass

        cidFile = open("ClientIDs.txt", "a")
        cidFile.write(f"{cid}\n")
        cidFile.close()

        await ctx.send(f"User ID {cid} whitelisted!")
    
    @commands.command()
    async def removeUser(self, ctx, *cid):
        await self.IDCheck(ctx.author.id)

        if self.canuse == False:
            await ctx.send("You do not have permission to use this feature.")
            return
        
        if len(list(cid)) == 0:
            embed = discord.Embed(title="Removing Users", description=f"Using the removeUser command is as simple as inputting the user's Discord ID.\n{prefix}removeUser [UserID]", colour=0xe67e22, timestamp=datetime.datetime.utcnow())
            embed.set_image(url="https://cdn.discordapp.com/attachments/1052059625752629258/1052720946034782268/image.png")
            await ctx.send(embed = embed)
            return

        cidFileCheck = open("ClientIDs.txt", "r").readlines()
        cidFile = open("ClientIDs.txt", "w")

        for line in cidFileCheck:

            line = line.split("\n")[0]
            if line == cid:
                pass
            else:
                cidFile.write(f"{line}\n")

        await ctx.send(f"User ID {cid} un-whitelisted!")

    @commands.command()
    async def addAdmin(self, ctx, *cid):
        await self.IDCheck(ctx.author.id)

        if self.canuse == False:
            await ctx.send("You do not have permission to use this feature.")
            return
        
        if len(list(cid)) == 0:
            embed = discord.Embed(title="Adding admins", description=f"Using the addAdmin command is as simple as inputting the user's Discord ID.\n{prefix}addAdmin [UserID]", colour=0xe67e22, timestamp=datetime.datetime.utcnow())
            embed.set_image(url="https://cdn.discordapp.com/attachments/1052059625752629258/1052720946034782268/image.png")
            await ctx.send(embed = embed)
            return

        cidFileCheck = open("AdminIDs.txt", "r").readlines()

        for line in cidFileCheck:
            line = line.strip("\n")
            if line == cid:
                await ctx.send(f"User ID {cid} is already an admin.")
                return
            else:
                pass

        cidFile = open("AdminIDs.txt", "a")
        cidFile.write(f"{cid}\n")
        cidFile.close()

        await ctx.send(f"User ID {cid} is now an admin!")

    @commands.command()
    async def removeAdmin(self, ctx, *cid):
        await self.IDCheck(ctx.author.id)

        if self.canuse == False:
            await ctx.send("You do not have permission to use this feature.")
            return
        
        if len(list(cid)) == 0:
            embed = discord.Embed(title="Removing Admins", description=f"Using the removeAdmin command is as simple as inputting the user's Discord ID.\n{prefix}removeAdmin [UserID]", colour=0xe67e22, timestamp=datetime.datetime.utcnow())
            embed.set_image(url="https://cdn.discordapp.com/attachments/1052059625752629258/1052720946034782268/image.png")
            await ctx.send(embed = embed)
            return

        cidFileCheck = open("AdminIDs.txt", "r").readlines()
        cidFile = open("AdminIDs.txt", "w")

        for line in cidFileCheck:

            line = line.split("\n")[0]
            if line == cid:
                pass
            else:
                cidFile.write(f"{line}\n")

        await ctx.send(f"User ID {cid} un-whitelisted!")
            
async def setup(bot):
    await bot.add_cog(Whitelister(bot))
from discord.ext import commands, tasks
import discord
import datetime
import asyncio

prefix = open("prefix.txt", "r").read()

class Whitelister(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.ids = []
        self.canuse = False
        self.date = datetime.datetime.today().strftime("%Y-%m-%d-%H:%M")

    @commands.Cog.listener()
    async def on_ready(self):
        print("Whitelister cog loaded.")
        self.ExpiryCheck.start()

    @tasks.loop(seconds=5)
    async def ExpiryCheck(self):
        idFile = open("./IDs/ClientIDs.txt", "r").readlines()
        idFileToWrite = open("./IDs/ClientIDs.txt", "w")

        for line in idFile:
            line = line.split("\n")
            lineToWrite = line[0]
            line = line[0].split("=")

            dateCheck = line[1].split("-")
            dateCheckHour = dateCheck[3].split(":")
            clientDate = datetime.datetime.today().replace(year=int(dateCheck[0]), month=int(dateCheck[1]), day=int(dateCheck[2]), hour=int(dateCheckHour[0]), minute=int(dateCheckHour[1]))
            ExpirationDate = clientDate + datetime.timedelta(days=int(line[2]))
            
            if ExpirationDate < datetime.datetime.now():
                pass
            else:
                idFileToWrite.write(f"{lineToWrite}\n")
    
    async def IDCheck(self, uid):
        idFile = open("./IDs/AdminIDs.txt", "r").readlines()

        for line in idFile:
            line = line.split("\n")
            line = line[0].split(":")
            if line[0] != str(uid):
                self.canuse = False
            else:
                self.canuse = True
                return

    @commands.command(aliases=["adduser"])
    async def addUser(self, ctx, *args):
        args = list(args)
        await self.IDCheck(ctx.author.id)
        if self.canuse == False:
            await ctx.send("You do not have permission to use this feature.")
            return

        if len(args) == 0:
            embed = discord.Embed(title="Adding Users", description=f"Using the addUsers command is as simple as inputting the user's Discord ID.\n{prefix}addUser [UserID] [(Optional) Length of whitelist (in days). Default = 14]", colour=0xe67e22, timestamp=datetime.datetime.utcnow())
            embed.set_image(url="https://cdn.discordapp.com/attachments/1052059625752629258/1052720946034782268/image.png")
            await ctx.send(embed = embed)
            return
        
        if len(args) == 1:
            args.append("14")
        
        cid = args[0]
        cidFileCheck = open("./IDs/ClientIDs.txt", "r").readlines()
        cidFile = open("./IDs/ClientIDs.txt", "a")

        for line in cidFileCheck:
            line = line.strip("\n")
            line = line.split("=")
            if line[0] == cid:
                await ctx.send(f"User ID {cid} already whitelited.")
                return
            else:
                pass
        
        cidFile.write(f"{cid}={self.date}={args[1]}\n")
        cidFile.close()

        await ctx.send(f"User ID {cid} whitelisted!")
    
    @commands.command(aliases=["removeuser"])
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

        cid = list(cid)[0]
        cidFileCheck = open("./IDs/ClientIDs.txt", "r").readlines()
        cidFile = open("./IDs/ClientIDs.txt", "w")

        for line in cidFileCheck:

            line = line.split("\n")[0]
            line = line[0].strip("=")
            if line[0] == cid:
                pass
            else:
                cidFile.write(f"{line}\n")

        await ctx.send(f"User ID {cid} un-whitelisted!")

    @commands.command(aliases=["addadmin"])
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

        cid = list(cid)[0]
        cidFileCheck = open("./IDs/AdminIDs.txt", "r").readlines()
        cidFile = open("./IDs/AdminIDs.txt", "a")

        for line in cidFileCheck:
            line = line.strip("\n")
            line = line.strip("=")
            if line[0] == cid:
                await ctx.send(f"User ID {cid} is already an admin.")
                return
            else:
                pass

        cidFile.write(f"{cid}\n")
        cidFile.close()

        await ctx.send(f"User ID {cid} is now an admin!")

    @commands.command(aliases=["removeadmin"])
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

        cid = list(cid)[0]
        cidFileCheck = open("./IDs/AdminIDs.txt", "r").readlines()
        cidFile = open("./IDs/AdminIDs.txt", "w")

        for line in cidFileCheck:

            line = line.split("\n")[0]
            line = line.split("=")
            if line[0] == cid:
                pass
            else:
                cidFile.write(f"{line}\n")

        await ctx.send(f"User ID {cid} un-whitelisted!")
            
async def setup(bot):
    await bot.add_cog(Whitelister(bot))
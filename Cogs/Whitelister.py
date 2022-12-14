from discord.ext import commands

prefix = open("prefix.txt", "r").read()

class Whitelister(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.ids = []

    @commands.Cog.listener()
    async def on_ready(self):
        print("Whitelister cog loaded.")

    @commands.command()
    async def addUser(self, ctx, cid):

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
    async def removeUser(self, ctx, cid):

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
    async def addAdmin(self, ctx, cid):

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
    async def removeAdmin(self, ctx, cid):

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
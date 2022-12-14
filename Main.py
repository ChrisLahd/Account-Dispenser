# Account Dispenser
import discord
from discord.ext import commands
import os
import asyncio

intents = discord.Intents.all()
prefix = open("prefix.txt", "r").read()
bot = commands.Bot(command_prefix=prefix, description="Account Dispensory", intents=intents)

async def loadOnStartup():
    for filename in os.listdir("./Cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"Cogs.{filename[:-3]}")

@bot.remove_command("help")

@bot.command()
async def load(ctx, cog):
    await bot.load_extension(f"Cogs.{cog}")

@bot.command()
async def unload(ctx, cog):
    await bot.unload_extension(f"Cogs.{cog}")

@bot.command()
async def reload(ctx, cog):

    if cog == "all":
        for filename in os.listdir("./Cogs"):
            if filename.endswith(".py"):
               await bot.unload_extension(f"Cogs.{filename[:-3]}")
               await bot.load_extension(f"Cogs.{filename[:-3]}")
    else:
        await bot.unload_extension(f"Cogs.{cog}")
        await bot.load_extension(f"Cogs.{cog}")

async def main():
    await loadOnStartup()
    await bot.start("MTA1MjA1MzI0MTYwNjcwOTI3OQ.G1l4Ju.Gv-c08H9Qd4SC3X7OFwEVMbEet8wJWL-JPnWcE")

asyncio.run(main())
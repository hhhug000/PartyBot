import discord
from dotenv import load_dotenv
import os
import asyncio
from discord.ext import commands

load_dotenv()

token = os.getenv("TOKEN")

intents = discord.Intents.default()

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    try:
        synced = await bot.tree.sync()
        print(f"synced {len(synced)} commands")
    except Exception as e:
        print(f"Failed to sync commands, error: {e}")

async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"Loaded cog {filename[:-3]}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(token)

asyncio.run(main())
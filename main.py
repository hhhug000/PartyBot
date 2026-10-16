import discord
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv("TOKEN")

intents = discord.Intents.default()

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

client.run(token)
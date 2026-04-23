import os

import discord
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

if not TOKEN:
    raise ValueError("DISCORD_BOT_TOKEN is missing from the .env file.")


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def onready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("CyberOps Bot is online.")


bot.run(TOKEN)
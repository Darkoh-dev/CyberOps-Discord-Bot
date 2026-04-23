import json
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv


SETTINGS_PATH = "config/settings.json"

load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

if not TOKEN:
    raise ValueError("DISCORD_BOT_TOKEN is missing from the .env file.")

with open (SETTINGS_PATH, "r", encoding="utf-8") as settings_file:
    settings = json.load(settings_file)

COMMAND_PREFIX = settings.get("command_prefix", "!")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print(f"{settings.get('bot_name', 'CyberOps Bot')} is online.")
    print(f"Using command prefix: {COMMAND_PREFIX}")


@bot.command(name="ping")
async def ping(ctx):
    await ctx.send("CyberOps Bot is responding.")


bot.run(TOKEN)
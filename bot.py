import json
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from commands.threat_commands import setup_threat_commands
from commands.log_commands import setup_log_commands
from commands.link_commands import setup_link_commands


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



setup_threat_commands(bot, settings)
setup_log_commands(bot, settings)
setup_link_commands(bot)

@bot.command(name="helpme")
async def helpme(ctx):
    await ctx.send(
        "CyberOps Bot Commands:\n"
        "!threats [category] [severity] - View threat items\n"
        "!analyzelog <log text> - Analyze pasted log text\n"
        "!inspectlink <url> - Inspect a link for basic red flags\n"
        "Examples:\n"
        "!threats cve critical\n"
        "!analyzelog Failed password for invalid user admin\n"
        "!inspectlink example.com/login"
    )

bot.run(TOKEN)
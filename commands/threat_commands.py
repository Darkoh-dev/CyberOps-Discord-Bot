from discord.ext import commands


def setup_threat_commands(bot):
    @bot.command(name="ping")
    async def ping(ctx):
       await ctx.send("CyberOps Bot is responding.")
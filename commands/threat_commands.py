from discord.ext import commands


def setup_threat_commands(bot):
    @bot.command(name="threats")
    async def threats(ctx):
        await ctx.send("Threat alert module is conneted and ready.")
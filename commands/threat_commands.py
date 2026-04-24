from discord.ext import commands

from services.threat_service import get_threat_items

def setup_threat_commands(bot):
    @bot.command(name="threats")
    async def threats(ctx, category=None, severity=None):
        threat_items = get_threat_items(category=category, severity=severity)

        if not threat_items:
            await ctx.send("No threat items matched your filters.")
            return
        
        lines = []

        for item in threat_items:
            lines.append(
                f"[{item['severity'].upper()}] {item['title']} "
                f"({item['category']})\n"
                f"Source: {item['source']}\n"
                f"Summary: {item['summary']}\n"
                f"URL: {item['url']}"
            )

        message = "\n\n".join(lines)

        await ctx.send(message)
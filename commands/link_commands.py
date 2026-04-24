from services.link_service import inspect_url


def setup_link_commands(bot):
    @bot.command(name="inspectlink")
    async def inspect_link(ctx, url=None):
        if not url:
            await ctx.send("Usage: !inspectlink <url>")
            return
        
        result = inspect_url(url)

        lines = [
            f"Link Inspection Results:",
            f"URL: {result['normalized_url']}",
            f"Host: {result['hostname'] or 'Unavailable'}"
        ]

        if result["findings"]:
            lines.append("Findings:")

            for finding in result["findings"]:
                lines.append(f"- {finding}")
            else:
                lines.append("Findings:")
                lines.append("- No obvious formatting red flags were detected.")

            lines.append("Caution Notes:")

            for note in result["caution_notes"]:
                lines.append(f"- {note}")

            await ctx.send("\n".join(lines))
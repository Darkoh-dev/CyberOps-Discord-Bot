from services.threat_service import get_threat_items


VALID_CATEGORIES = {"news", "cve", "breach"}
VALID_SEVERITIES = {"low", "medium", "high", "critical"}


def setup_threat_commands(bot, settings):
    @bot.command(name="threats")
    async def threats(ctx, first_filer=None, second_filter=None):
        category = None
        severity = None

        for value in [first_filer, second_filter]:
            if not value:
                continue

            normalized_value = value.lower()

            if normalized_value in VALID_CATEGORIES:
                category = normalized_value
            elif normalized_value in VALID_SEVERITIES:
                severity = normalized_value
            else:
                await ctx.send(
                    "Usage: !threats [category] [severity]\n"
                    "Valid categories: news, cve, breach\n"
                    "Valid severities: low, medium, high, critical"
                )
                return
            
        limit = settings.get("limits", {}).get("max_threat_results", 5)
        threat_items = get_threat_items(
            category=category,
            severity=severity,
            limit=limit
        )

        if not threat_items:
            await ctx.send("No threat items matched your filters.")
            return
        
        lines = ["Threat Alert Results:"]

        for item in threat_items:
            lines.append(
                f"[{item['severity'].upper()}] {item['title']} "
                f"({item['category']})\n"
                f"Source: {item['source']}\n"
                f"Summary: {item['summary']}\n"
                f"URL: {item['url']}"
            )

        await ctx.send("\n\n".join(lines))
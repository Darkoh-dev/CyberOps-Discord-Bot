from services.log_service import analyze_log_text


def setup_log_commands(bot):
    @bot.command(name="analyzelog")
    async def analyze_log(ctx, *, log_text=None):
        if not log_text:
            await ctx.send(
                "Usage: !analyzelog <paste log text here>"
            )
            return
        
        findings = analyze_log_text(log_text)

        if not findings:
            await ctx.send(
                "No suspicious rule matches were found in the submitted log text."
            )
            return
        
        lines = ["Log Analysis Results:"]

        for finding in findings:
            lines.append(
                f"[{finding['severity'].upper()}] {finding['name']}: "
                f"{finding['description']}"
            )

        await ctx.send("\n".join(lines))
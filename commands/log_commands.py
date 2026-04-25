from services.log_service import analyze_log_text


def setup_log_commands(bot, settings):
    @bot.command(name="analyzelog")
    async def analyze_log(ctx, *, log_text=None):
        max_log_chars = settings.get("limits", {}).get("max_log_chars", 4000)
        max_attachment_bytes = settings.get("limits", {}).get("max_log_attachment_bytes", 50000)

        if not log_text and not ctx.message.attachments:
            await ctx.send(
                "Usage: !analyzelog <paste log text here>\n"
                "You can also attach a small .txt or .log file with the command."
            )
            return
        
        if log_text and len(log_text) > max_log_chars:
            await ctx.send(
                f"Submitted log text is too long. Limit: {max_log_chars} characters."
            )
            return
        
        if not log_text and ctx.message.attachments:
            attachment = ctx.message.attachments[0]

            if attachment.size > max_attachment_bytes:
                await ctx.send(
                    f"Attached file is too large. Limit: {max_attachment_bytes} bytes."
                )
                return
            
            if not attachment.filename.lower().endswith((".txt", ".log")):
                await ctx.send(
                    "Only .txt and .log attachments are supported."
                )
                return
            
            attachment_bytes = await attachment.read()
            log_text = attachment_bytes.decode("utf-8", errors="ignore")

        analysis_result = analyze_log_text(log_text)
        findings = analysis_result["findings"]
        line_count = analysis_result["line_count"]

        if not findings:
            await ctx.send(
                "No suspicious rule matches were found in the submitted log text."
            )
            return
        
        lines = [
            "Log Analysis Results:",
            f"Lines Reviewed: {line_count}",
            f"Findings Count: {len(findings)}"
        ]

        for finding in findings:
            lines.append(
                f"[{finding['severity'].upper()}] {finding['name']}: "
                f"{finding['description']}"
            )

        await ctx.send("\n".join(lines))
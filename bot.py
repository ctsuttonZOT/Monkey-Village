from discord.ext import commands
import discord
import settings

logger = settings.logging.getLogger("bot")

CHANNEL_ID = 1232929274571526174

def main():
    bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())

    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")

    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

if __name__ == "__main__":
    main()

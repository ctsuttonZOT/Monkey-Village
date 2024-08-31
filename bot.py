import discord
from discord.ext import commands
import settings

logger = settings.logging.getLogger("bot")

def main():
    bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")

        await bot.load_extension("cogs.registration")
        await bot.load_extension("cogs.player_stats")

        await bot.tree.sync()

    bot.run(settings.DISCORD_API_SECRET, root_logger=True)


if __name__ == "__main__":
    main()

import discord
from discord.ext import commands
import settings
from ninja_kiwi_api import NinjaKiwiApi
from database import Database

logger = settings.logging.getLogger("bot")

# Hardcoded now for testing, will be changed when bot is ready.
CHANNEL_ID = 1232929274571526174

def main():
    bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")
        global db
        db = Database()


    @bot.command()
    async def register(ctx, oak):
        db.add_user(str(ctx.author), oak)
        await ctx.send(f"User '{str(ctx.author)}' successfully registered.")


    @bot.command()
    async def get_monkey_money(ctx, username = None):
        try:
            if username:
                api = NinjaKiwiApi(db.retrieve_user_oak(username))
                api.load_data()
                await ctx.send(f"{username} has {api.monkey_money} Monkey Money!")
            else:
                api = NinjaKiwiApi(db.retrieve_user_oak(str(ctx.author)))
                api.load_data()
                await ctx.send(f"You have {api.monkey_money} Monkey Money!")
        except TypeError:
            await ctx.send("Data for this user cannot be retrieved.")
    
    bot.run(settings.DISCORD_API_SECRET, root_logger=True)


if __name__ == "__main__":
    main()

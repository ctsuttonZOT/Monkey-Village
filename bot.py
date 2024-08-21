import discord
from discord.ext import commands
import settings
import sqlite3
import io
import aiohttp
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
        api = NinjaKiwiApi(oak)
        if not api.valid_oak_check():
            await ctx.send("The OAK given is invalid.")
        else:
            try:
                db.add_user(str(ctx.author), oak)
                await ctx.send(f"User '{str(ctx.author)}' successfully registered.")
            except sqlite3.IntegrityError:
                await ctx.send("This user is already registered!")
    
    @bot.command()
    async def deregister(ctx):
        db.remove_user(str(ctx.author))
        await ctx.send(f"User '{str(ctx.author)}' deregistered.")


    @bot.command()
    async def monkey_money(ctx, username = None):
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
            await ctx.send("Data for this user cannot be retrieved. Perhaps an invalid OAK was given.")
        except KeyError:
            await ctx.send("Data for this user cannot be retrieved. Perhaps an invalid OAK was given.")
    
    @bot.command()
    async def current_hero(ctx, username = None):
        try:
            if username:
                api = NinjaKiwiApi(db.retrieve_user_oak(username))
                api.load_data()
                await ctx.send(f"{username} is currently using {api.current_hero} as their hero!")
            else:
                api = NinjaKiwiApi(db.retrieve_user_oak(str(ctx.author)))
                api.load_data()
                await ctx.send(f"You currently have {api.current_hero} as your hero!")
        except TypeError:
            await ctx.send("Data for this user cannot be retrieved.")
        except KeyError:
            await ctx.send("Data for this user cannot be retrieved. Perhaps an invalid OAK was given.")
    
    @bot.command()
    async def level(ctx, username = None):
        try:
            if username:
                api = NinjaKiwiApi(db.retrieve_user_oak(username))
                api.load_data()
                await ctx.send(f"{username} is level {api.rank}.")
            else:
                api = NinjaKiwiApi(db.retrieve_user_oak(str(ctx.author)))
                api.load_data()
                await ctx.send(f"You are level {api.rank}.")
        except TypeError:
            await ctx.send("Data for this user cannot be retrieved.")
        except KeyError:
            await ctx.send("Data for this user cannot be retrieved. Perhaps an invalid OAK was given.")
    
    @bot.command()
    async def favorite_monkey(ctx, username = None):
        try:
            if username:
                api = NinjaKiwiApi(db.retrieve_user_oak(username))
                api.load_data()
                await ctx.send(f"{username}'s favorite monkey is the {api.fav_monkey}!")
            else:
                api = NinjaKiwiApi(db.retrieve_user_oak(str(ctx.author)))
                api.load_data()
                await ctx.send(f"Your favorite monkey is the {api.fav_monkey}!")
        except TypeError:
            await ctx.send("Data for this user cannot be retrieved.")
        except KeyError:
            await ctx.send("Data for this user cannot be retrieved. Perhaps an invalid OAK was given.")
    
    @bot.command()
    async def favorite_hero(ctx, username = None):
            try:
                if username:
                    api = NinjaKiwiApi(db.retrieve_user_oak(username))
                    api.load_data()
                    await ctx.send(f"{username}'s favorite hero is {api.fav_hero}!")
                else:
                    api = NinjaKiwiApi(db.retrieve_user_oak(str(ctx.author)))
                    api.load_data()
                    await ctx.send(f"Your favorite hero is {api.fav_hero}!")
            except TypeError:
                await ctx.send("Data for this user cannot be retrieved.")
            except KeyError:
                await ctx.send("Data for this user cannot be retrieved. Perhaps an invalid OAK was given.")
    
    @bot.command()
    async def bloons_popped(ctx, username = None):
        try:
            if username:
                api = NinjaKiwiApi(db.retrieve_user_oak(username))
                api.load_data()
                await ctx.send(f"{username} has popped {api.bloons_popped:,} bloons!")
            else:
                api = NinjaKiwiApi(db.retrieve_user_oak(str(ctx.author)))
                api.load_data()
                await ctx.send(f"You have popped {api.bloons_popped:,} bloons!")
        except TypeError:
            await ctx.send("Data for this user cannot be retrieved.")
        except KeyError:
            await ctx.send("Data for this user cannot be retrieved. Perhaps an invalid OAK was given.")
    
    @bot.command()
    async def highest_round(ctx, username = None):
        try:
            if username:
                api = NinjaKiwiApi(db.retrieve_user_oak(username))
                api.load_data()
                await ctx.send(f"{username}'s highest round is {api.highest_round}!")
            else:
                api = NinjaKiwiApi(db.retrieve_user_oak(str(ctx.author)))
                api.load_data()
                await ctx.send(f"Your highest round is {api.highest_round}!")
        except TypeError:
            await ctx.send("Data for this user cannot be retrieved.")
        except KeyError:
            await ctx.send("Data for this user cannot be retrieved. Perhaps an invalid OAK was given.")
    
    @bot.command()
    async def black_borders(ctx, username = None):
        try:
            if username:
                api = NinjaKiwiApi(db.retrieve_user_oak(username))
                api.load_data()
                await ctx.send(f"{username} has {api.black_borders} black borders!")
            else:
                api = NinjaKiwiApi(db.retrieve_user_oak(str(ctx.author)))
                api.load_data()
                await ctx.send(f"You have {api.black_borders} black borders!")
        except TypeError:
            await ctx.send("Data for this user cannot be retrieved.")
        except KeyError:
            await ctx.send("Data for this user cannot be retrieved. Perhaps an invalid OAK was given.")
    
    @bot.command()
    async def avatar(ctx, username = None):
        try:
            if username:
                api = NinjaKiwiApi(db.retrieve_user_oak(username))
                api.load_data()
                async with aiohttp.ClientSession() as session:
                    async with session.get(api.avatar_url) as resp:
                        if resp.status != 200:
                            await ctx.send("Could not download file.")
                        data = io.BytesIO(await resp.read())
                        await ctx.send(f"{username}'s current avatar:", file=discord.File(data, 'user_avatar.png'))
            else:
                api = NinjaKiwiApi(db.retrieve_user_oak(str(ctx.author)))
                api.load_data()
                async with aiohttp.ClientSession() as session:
                    async with session.get(api.avatar_url) as resp:
                        if resp.status != 200:
                            await ctx.send("Could not download file.")
                        data = io.BytesIO(await resp.read())
                        await ctx.send("Your current avatar:", file=discord.File(data, 'user_avatar.png'))
        except TypeError:
            await ctx.send("Data for this user cannot be retrieved.")
        except KeyError:
            await ctx.send("Data for this user cannot be retrieved. Perhaps an invalid OAK was given.")

    @bot.command()
    async def stats(ctx, username = None):
        try:
            if username:
                api = NinjaKiwiApi(db.retrieve_user_oak(username))
                api.load_data()
                embed = discord.Embed(
                    color = discord.Colour.dark_embed(),
                    title = f"{username}'s Stats:",
                    description = f"""
                               \nLevel: {api.rank}
                               \nFavorite Monkey: {api.fav_monkey}
                               \nFavorite Hero: {api.fav_hero}
                               \nHighest Round: {api.highest_round}
                               \nBloons Popped: {api.bloons_popped:,}
                               \nBlack Borders: {api.black_borders}
                                """)
                embed.set_thumbnail(url=api.avatar_url)
                await ctx.send(embed=embed)
            else:
                api = NinjaKiwiApi(db.retrieve_user_oak(str(ctx.author)))
                api.load_data()
                embed = discord.Embed(
                    color = discord.Colour.dark_embed(),
                    title = f"{ctx.author}'s Stats:",
                    description = f"""
                               \nLevel: {api.rank}
                               \nFavorite Monkey: {api.fav_monkey}
                               \nFavorite Hero: {api.fav_hero}
                               \nHighest Round: {api.highest_round}
                               \nBloons Popped: {api.bloons_popped:,}
                               \nBlack Borders: {api.black_borders}
                                """)
                embed.set_thumbnail(url=api.avatar_url)
                await ctx.send(embed=embed)
        except TypeError:
            await ctx.send("Data for this user cannot be retrieved.")
        except KeyError:
            await ctx.send("Data for this user cannot be retrieved. Perhaps an invalid OAK was given.")
    
    bot.run(settings.DISCORD_API_SECRET, root_logger=True)


if __name__ == "__main__":
    main()

import discord
import asyncio
from discord.ext import commands
import settings
import sqlite3
import io
import aiohttp
from ninja_kiwi_api import NinjaKiwiApi
from database import Database

logger = settings.logging.getLogger("bot")

def main():
    bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")

        global db
        db = Database()

        await bot.tree.sync()

    @bot.hybrid_command()
    async def register(ctx: commands.Context, oak: str):
        api = NinjaKiwiApi(oak)
        if not api.valid_oak_check():
            await ctx.send("The OAK given is invalid.")
        else:
            try:
                db.add_user(str(ctx.author), oak)
                await ctx.send(f"User {ctx.author.mention} successfully registered.", silent=True)
            except sqlite3.IntegrityError:
                await ctx.send("This user is already registered!")
    
    @bot.hybrid_command()
    async def deregister(ctx: commands.Context):
        db.remove_user(str(ctx.author))
        await ctx.send(f"User {ctx.author.mention} deregistered.", silent=True)


    @bot.hybrid_command()
    async def monkey_money(ctx: commands.Context, username: str = None):
        try:
            if username:
                api = NinjaKiwiApi(db.retrieve_user_oak(username))
                api.load_data()
                user = discord.utils.get(ctx.guild.members, name = username)
                await ctx.send(f"{user.mention} has {api.monkey_money} Monkey Money!", silent=True)
            else:
                api = NinjaKiwiApi(db.retrieve_user_oak(str(ctx.author)))
                api.load_data()
                await ctx.send(f"{ctx.author.mention} has {api.monkey_money} Monkey Money!", silent=True)
        except TypeError:
            await ctx.send("Data for this user cannot be retrieved. Perhaps an invalid OAK was given.")
        except KeyError:
            await ctx.send("Data for this user cannot be retrieved. Perhaps an invalid OAK was given.")
    
    @bot.hybrid_command()
    async def current_hero(ctx: commands.Context, username: str = None):
        try:
            if username:
                api = NinjaKiwiApi(db.retrieve_user_oak(username))
                api.load_data()
                user = discord.utils.get(ctx.guild.members, name = username)
                await ctx.defer()
                await asyncio.sleep(4)
                await ctx.send(f"{user.mention} is currently using {api.current_hero} as their hero!", silent=True)
            else:
                api = NinjaKiwiApi(db.retrieve_user_oak(str(ctx.author)))
                api.load_data()
                await ctx.defer()
                await asyncio.sleep(4)
                await ctx.send(f"{ctx.author.mention} currently has {api.current_hero} as their hero!", silent=True)
        except TypeError:
            await ctx.send("Data for this user cannot be retrieved.")
        except KeyError:
            await ctx.send("Data for this user cannot be retrieved. Perhaps an invalid OAK was given.")
    
    @bot.hybrid_command()
    async def level(ctx: commands.Context, username: str = None):
        try:
            if username:
                api = NinjaKiwiApi(db.retrieve_user_oak(username))
                api.load_data()
                user = discord.utils.get(ctx.guild.members, name = username)
                await ctx.send(f"{user.mention} is level {api.rank}.", silent=True)
            else:
                api = NinjaKiwiApi(db.retrieve_user_oak(str(ctx.author)))
                api.load_data()
                await ctx.send(f"{ctx.author.mention} is level {api.rank}.", silent=True)
        except TypeError:
            await ctx.send("Data for this user cannot be retrieved.")
        except KeyError:
            await ctx.send("Data for this user cannot be retrieved. Perhaps an invalid OAK was given.")
    
    @bot.hybrid_command()
    async def favorite_monkey(ctx: commands.Context, username: str = None):
        try:
            if username:
                api = NinjaKiwiApi(db.retrieve_user_oak(username))
                api.load_data()
                user = discord.utils.get(ctx.guild.members, name = username)
                await ctx.defer()
                await asyncio.sleep(5)
                await ctx.send(f"{user.mention}'s favorite monkey is the {api.fav_monkey}!", silent=True)
            else:
                api = NinjaKiwiApi(db.retrieve_user_oak(str(ctx.author)))
                api.load_data()
                await ctx.defer()
                await asyncio.sleep(5)
                await ctx.send(f"{ctx.author.mention}'s favorite monkey is the {api.fav_monkey}!", silent=True)
        except TypeError:
            await ctx.send("Data for this user cannot be retrieved.")
        except KeyError:
            await ctx.send("Data for this user cannot be retrieved. Perhaps an invalid OAK was given.")
    
    @bot.hybrid_command()
    async def favorite_hero(ctx: commands.Context, username: str = None):
            try:
                if username:
                    api = NinjaKiwiApi(db.retrieve_user_oak(username))
                    api.load_data()
                    user = discord.utils.get(ctx.guild.members, name = username)
                    await ctx.defer()
                    await asyncio.sleep(5)
                    await ctx.send(f"{user.mention}'s favorite hero is {api.fav_hero}!", silent=True)
                else:
                    api = NinjaKiwiApi(db.retrieve_user_oak(str(ctx.author)))
                    api.load_data()
                    await ctx.defer()
                    await asyncio.sleep(5)
                    await ctx.send(f"{ctx.author.mention}'s favorite hero is {api.fav_hero}!", silent=True)
            except TypeError:
                await ctx.send("Data for this user cannot be retrieved.")
            except KeyError:
                await ctx.send("Data for this user cannot be retrieved. Perhaps an invalid OAK was given.")
    
    @bot.hybrid_command()
    async def bloons_popped(ctx: commands.Context, username: str = None):
        try:
            if username:
                api = NinjaKiwiApi(db.retrieve_user_oak(username))
                api.load_data()
                user = discord.utils.get(ctx.guild.members, name = username)
                await ctx.send(f"{user.mention} has popped {api.bloons_popped:,} bloons!", silent=True)
            else:
                api = NinjaKiwiApi(db.retrieve_user_oak(str(ctx.author)))
                api.load_data()
                await ctx.send(f"{ctx.author.mention} has popped {api.bloons_popped:,} bloons!", silent=True)
        except TypeError:
            await ctx.send("Data for this user cannot be retrieved.")
        except KeyError:
            await ctx.send("Data for this user cannot be retrieved. Perhaps an invalid OAK was given.")
    
    @bot.hybrid_command()
    async def highest_round(ctx: commands.Context, username: str = None):
        try:
            if username:
                api = NinjaKiwiApi(db.retrieve_user_oak(username))
                api.load_data()
                user = discord.utils.get(ctx.guild.members, name = username)
                await ctx.send(f"{user.mention}'s highest round is {api.highest_round}!", silent=True)
            else:
                api = NinjaKiwiApi(db.retrieve_user_oak(str(ctx.author)))
                api.load_data()
                await ctx.send(f"{ctx.author.mention}'s highest round is {api.highest_round}!", silent=True)
        except TypeError:
            await ctx.send("Data for this user cannot be retrieved.")
        except KeyError:
            await ctx.send("Data for this user cannot be retrieved. Perhaps an invalid OAK was given.")
    
    @bot.hybrid_command()
    async def black_borders(ctx: commands.Context, username: str = None):
        try:
            if username:
                api = NinjaKiwiApi(db.retrieve_user_oak(username))
                api.load_data()
                user = discord.utils.get(ctx.guild.members, name = username)
                await ctx.send(f"{user.mention} has {api.black_borders} black borders!", silent=True)
            else:
                api = NinjaKiwiApi(db.retrieve_user_oak(str(ctx.author)))
                api.load_data()
                await ctx.send(f"{ctx.author.mention} has {api.black_borders} black borders!", silent=True)
        except TypeError:
            await ctx.send("Data for this user cannot be retrieved.")
        except KeyError:
            await ctx.send("Data for this user cannot be retrieved. Perhaps an invalid OAK was given.")
    
    @bot.hybrid_command()
    async def avatar(ctx: commands.Context, username: str = None):
        try:
            if username:
                api = NinjaKiwiApi(db.retrieve_user_oak(username))
                api.load_data()
                user = discord.utils.get(ctx.guild.members, name = username)
                async with aiohttp.ClientSession() as session:
                    async with session.get(api.avatar_url) as resp:
                        if resp.status != 200:
                            await ctx.send("Could not download file.")
                        data = io.BytesIO(await resp.read())
                        await ctx.defer()
                        await asyncio.sleep(4)
                        await ctx.send(f"{user.mention}'s current avatar:", file=discord.File(data, 'user_avatar.png'), silent=True)
            else:
                api = NinjaKiwiApi(db.retrieve_user_oak(str(ctx.author)))
                api.load_data()
                async with aiohttp.ClientSession() as session:
                    async with session.get(api.avatar_url) as resp:
                        if resp.status != 200:
                            await ctx.send("Could not download file.")
                        data = io.BytesIO(await resp.read())
                        await ctx.defer()
                        await asyncio.sleep(4)
                        await ctx.send(f"{ctx.author.mention}'s current avatar:", file=discord.File(data, 'user_avatar.png'), silent=True)
        except TypeError:
            await ctx.send("Data for this user cannot be retrieved.")
        except KeyError:
            await ctx.send("Data for this user cannot be retrieved. Perhaps an invalid OAK was given.")

    @bot.hybrid_command()
    async def stats(ctx: commands.Context, username: str = None):
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
                await ctx.defer()
                await asyncio.sleep(4)
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
                await ctx.defer()
                await asyncio.sleep(4)
                await ctx.send(embed=embed)
        except TypeError:
            await ctx.send("Data for this user cannot be retrieved.")
        except KeyError:
            await ctx.send("Data for this user cannot be retrieved. Perhaps an invalid OAK was given.")
    
    bot.run(settings.DISCORD_API_SECRET, root_logger=True)


if __name__ == "__main__":
    main()

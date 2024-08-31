import discord
import aiohttp
import io
from discord.ext import commands
from ninja_kiwi_api import NinjaKiwiApi
from database import Database

DB = Database()

class PlayerStats(commands.Cog, name="Player Stats"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(brief="Displays a user's current monkey money.",
                        description="Displays the monkey money of the user who uses the command, or of the user whose username is given.")
    async def monkey_money(self, ctx: commands.Context, username: str = None):
        try:
            if username:
                api = NinjaKiwiApi(DB.retrieve_user_oak(username))
                api.load_data()
                user = discord.utils.get(ctx.guild.members, name = username)
                await ctx.interaction.response.defer()
                await ctx.interaction.followup.send(f"{user.mention} has {api.monkey_money} Monkey Money!")
            else:
                api = NinjaKiwiApi(DB.retrieve_user_oak(str(ctx.author)))
                api.load_data()
                await ctx.interaction.response.defer()
                await ctx.interaction.followup.send(f"{ctx.author.mention} has {api.monkey_money} Monkey Money!")
        except TypeError:
            await ctx.send("Data for this user cannot be retrieved. Perhaps an invalid OAK was given.")
        except KeyError:
            await ctx.send("Data for this user cannot be retrieved. Perhaps an invalid OAK was given.")
    
    @commands.hybrid_command(brief="Displays a user's currently selected hero.",
                        description="Displays the current hero of the user who uses the command, or of the user whose username is given.")
    async def current_hero(self, ctx: commands.Context, username: str = None):
        try:
            if username:
                api = NinjaKiwiApi(DB.retrieve_user_oak(username))
                api.load_data()
                user = discord.utils.get(ctx.guild.members, name = username)
                await ctx.interaction.response.defer()
                await ctx.interaction.followup.send(f"{user.mention} is currently using {api.current_hero} as their hero!")
            else:
                api = NinjaKiwiApi(DB.retrieve_user_oak(str(ctx.author)))
                api.load_data()
                await ctx.interaction.response.defer()
                await ctx.interaction.followup.send(f"{ctx.author.mention} currently has {api.current_hero} as their hero!")
        except TypeError:
            await ctx.send("Data for this user cannot be retrieved.")
        except KeyError:
            await ctx.send("Data for this user cannot be retrieved. Perhaps an invalid OAK was given.")
    
    @commands.hybrid_command(brief="Displays a user's current level.",
                        description="Displays the current level of the user who uses the command, or of the user whose username is given.")
    async def level(self, ctx: commands.Context, username: str = None):
        try:
            if username:
                api = NinjaKiwiApi(DB.retrieve_user_oak(username))
                api.load_data()
                user = discord.utils.get(ctx.guild.members, name = username)
                await ctx.interaction.response.defer()
                await ctx.interaction.followup.send(f"{user.mention} is level {api.rank}.")
            else:
                api = NinjaKiwiApi(DB.retrieve_user_oak(str(ctx.author)))
                api.load_data()
                await ctx.interaction.response.defer()
                await ctx.interaction.followup.send(f"{ctx.author.mention} is level {api.rank}.")
        except TypeError:
            await ctx.send("Data for this user cannot be retrieved.")
        except KeyError:
            await ctx.send("Data for this user cannot be retrieved. Perhaps an invalid OAK was given.")
    
    @commands.hybrid_command(brief="Displays a user's favorite tower.",
                        description="Shows the favorite tower of the user who uses the command, or of the person whose username is given.")
    async def favorite_monkey(self, ctx: commands.Context, username: str = None):
        try:
            if username:
                api = NinjaKiwiApi(DB.retrieve_user_oak(username))
                api.load_data()
                user = discord.utils.get(ctx.guild.members, name = username)
                await ctx.interaction.response.defer()
                await ctx.interaction.followup.send(f"{user.mention}'s favorite monkey is the {api.fav_monkey}!")
            else:
                api = NinjaKiwiApi(DB.retrieve_user_oak(str(ctx.author)))
                api.load_data()
                await ctx.interaction.response.defer()
                await ctx.interaction.followup.send(f"{ctx.author.mention}'s favorite monkey is the {api.fav_monkey}!")
        except TypeError:
            await ctx.send("Data for this user cannot be retrieved.")
        except KeyError:
            await ctx.send("Data for this user cannot be retrieved. Perhaps an invalid OAK was given.")
    
    @commands.hybrid_command(brief="Displays a user's most used hero.",
                        description="Shows the favorite hero of the user who uses the command, or of the person whose username is given.")
    async def favorite_hero(self, ctx: commands.Context, username: str = None):
            try:
                if username:
                    api = NinjaKiwiApi(DB.retrieve_user_oak(username))
                    api.load_data()
                    user = discord.utils.get(ctx.guild.members, name = username)
                    await ctx.interaction.response.defer()
                    await ctx.interaction.followup.send(f"{user.mention}'s favorite hero is {api.fav_hero}!")
                else:
                    api = NinjaKiwiApi(DB.retrieve_user_oak(str(ctx.author)))
                    api.load_data()
                    await ctx.interaction.response.defer()
                    await ctx.interaction.followup.send(f"{ctx.author.mention}'s favorite hero is {api.fav_hero}!")
            except TypeError:
                await ctx.send("Data for this user cannot be retrieved.")
            except KeyError:
                await ctx.send("Data for this user cannot be retrieved. Perhaps an invalid OAK was given.")
    
    @commands.hybrid_command(brief="Displays a user's total number of bloons popped.",
                        description="Displays the pop count of the user who uses the command, or of the person whose username is given.")
    async def bloons_popped(self, ctx: commands.Context, username: str = None):
        try:
            if username:
                api = NinjaKiwiApi(DB.retrieve_user_oak(username))
                api.load_data()
                user = discord.utils.get(ctx.guild.members, name = username)
                await ctx.interaction.response.defer()
                await ctx.interaction.followup.send(f"{user.mention} has popped {api.bloons_popped:,} bloons!")
            else:
                api = NinjaKiwiApi(DB.retrieve_user_oak(str(ctx.author)))
                api.load_data()
                await ctx.interaction.response.defer()
                await ctx.interaction.followup.send(f"{ctx.author.mention} has popped {api.bloons_popped:,} bloons!")
        except TypeError:
            await ctx.send("Data for this user cannot be retrieved.")
        except KeyError:
            await ctx.send("Data for this user cannot be retrieved. Perhaps an invalid OAK was given.")
    
    @commands.hybrid_command(brief="Displays a user's highest seen round.",
                        description="Shows the highest round of the user who uses the command, or of the person whose username is given.")
    async def highest_round(self, ctx: commands.Context, username: str = None):
        try:
            if username:
                api = NinjaKiwiApi(DB.retrieve_user_oak(username))
                api.load_data()
                user = discord.utils.get(ctx.guild.members, name = username)
                await ctx.interaction.response.defer()
                await ctx.interaction.followup.send(f"{user.mention}'s highest round is {api.highest_round}!")
            else:
                api = NinjaKiwiApi(DB.retrieve_user_oak(str(ctx.author)))
                api.load_data()
                await ctx.interaction.response.defer()
                await ctx.interaction.followup.send(f"{ctx.author.mention}'s highest round is {api.highest_round}!")
        except TypeError:
            await ctx.send("Data for this user cannot be retrieved.")
        except KeyError:
            await ctx.send("Data for this user cannot be retrieved. Perhaps an invalid OAK was given.")
    
    @commands.hybrid_command(brief="Displays a user's total number of black borders.",
                        description="Shows the author's total number of black borders, or of the person whose username is given.")
    async def black_borders(self, ctx: commands.Context, username: str = None):
        try:
            if username:
                api = NinjaKiwiApi(DB.retrieve_user_oak(username))
                api.load_data()
                user = discord.utils.get(ctx.guild.members, name = username)
                await ctx.interaction.response.defer()
                await ctx.interaction.followup.send(f"{user.mention} has {api.black_borders} black borders!")
            else:
                api = NinjaKiwiApi(DB.retrieve_user_oak(str(ctx.author)))
                api.load_data()
                await ctx.interaction.response.defer()
                await ctx.interaction.followup.send(f"{ctx.author.mention} has {api.black_borders} black borders!")
        except TypeError:
            await ctx.send("Data for this user cannot be retrieved.")
        except KeyError:
            await ctx.send("Data for this user cannot be retrieved. Perhaps an invalid OAK was given.")
    
    @commands.hybrid_command(brief="Displays a user's currently equipped BTD6 avatar.",
                        description="Displays the avatar of the user who uses the command, or of the person whose username is given.")
    async def avatar(self, ctx: commands.Context, username: str = None):
        try:
            if username:
                api = NinjaKiwiApi(DB.retrieve_user_oak(username))
                api.load_data()
                user = discord.utils.get(ctx.guild.members, name = username)
                async with aiohttp.ClientSession() as session:
                    async with session.get(api.avatar_url) as resp:
                        if resp.status != 200:
                            await ctx.send("Could not download file.")
                        data = io.BytesIO(await resp.read())
                        await ctx.interaction.response.defer()
                        await ctx.interaction.followup.send(f"{user.mention}'s current avatar:", file=discord.File(data, 'user_avatar.png'))
            else:
                api = NinjaKiwiApi(DB.retrieve_user_oak(str(ctx.author)))
                api.load_data()
                async with aiohttp.ClientSession() as session:
                    async with session.get(api.avatar_url) as resp:
                        if resp.status != 200:
                            await ctx.send("Could not download file.")
                        data = io.BytesIO(await resp.read())
                        await ctx.interaction.response.defer()
                        await ctx.interaction.followup.send(f"{ctx.author.mention}'s current avatar:", file=discord.File(data, 'user_avatar.png'))
        except TypeError:
            await ctx.send("Data for this user cannot be retrieved.")
        except KeyError:
            await ctx.send("Data for this user cannot be retrieved. Perhaps an invalid OAK was given.")

    @commands.hybrid_command(brief="Displays various stats of the user.",
                        description="Shows various stats of the user who uses the command, or of the person whose username is given.")
    async def stats(self, ctx: commands.Context, username: str = None):
        try:
            if username:
                api = NinjaKiwiApi(DB.retrieve_user_oak(username))
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
                await ctx.interaction.response.defer()
                await ctx.interaction.followup.send(embed=embed)
            else:
                api = NinjaKiwiApi(DB.retrieve_user_oak(str(ctx.author)))
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
                await ctx.interaction.response.defer()
                await ctx.interaction.followup.send(embed=embed)
        except TypeError:
            await ctx.send("Data for this user cannot be retrieved.")
        except KeyError:
            await ctx.send("Data for this user cannot be retrieved. Perhaps an invalid OAK was given.")

async def setup(bot: commands.Bot):
    await bot.add_cog(PlayerStats(bot))

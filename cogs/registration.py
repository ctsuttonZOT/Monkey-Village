import discord
import sqlite3
from discord.ext import commands
from ninja_kiwi_api import NinjaKiwiApi
from database import Database

DB = Database()

class Registration(commands.Cog, name="Registration"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(brief="Registers a user in the bot's database.",
                        description="Registers a user in the bot's database when a valid OAK is given.")
    async def register(self, ctx: commands.Context, oak: str):
        api = NinjaKiwiApi(oak)
        if not api.valid_oak_check():
            await ctx.send("The OAK given is invalid.")
        else:
            try:
                DB.add_user(str(ctx.author), oak)
                await ctx.send(f"User {ctx.author.mention} successfully registered.")
            except sqlite3.IntegrityError:
                await ctx.send("This user is already registered!")
    
    @commands.hybrid_command(brief="Deregisters a user in the bot's database.",
                        description="Deregisters the user who uses the command from the bot's database.")
    async def deregister(self, ctx: commands.Context):
        DB.remove_user(str(ctx.author))
        await ctx.send(f"User {ctx.author.mention} deregistered.")

async def setup(bot: commands.Bot):
    await bot.add_cog(Registration(bot))

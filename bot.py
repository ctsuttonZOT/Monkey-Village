from discord.ext import commands
import discord

BOT_TOKEN = 'MTIzMjkwODk2MDAxNzY3ODQxOA.GmyFAY.WQTYsHCbVyoTYhV2MQqPDoBvGvE8xoS3WbPB_E'
CHANNEL_ID = 1232929274571526174

bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())

bot.run(BOT_TOKEN)

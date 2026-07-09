import os
import ast
import aiohttp
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

from api_bot import get_course_data

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

add_description = '''
do !add with a json string like this
    {
        'division': "ERIN", # string of division
        'sessions': "20259", # string of session ID
        'course_code': "CSC207H5", # string of course code
        'sections': ['PRA0107'] # a list sections
    }
full list can be found in pinned messages.
'''

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    check_courses.start()

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@tasks.loop(minutes=5)
async def check_courses():
    await get_course_data()

@bot.command()
async def run_api(ctx):
    await get_course_data()
    await ctx.send("API check started.")

bot.run(TOKEN)

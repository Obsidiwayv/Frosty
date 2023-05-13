from discord.ext import commands
from os import listdir

import discord
import json

with open("config.json", "r") as file:
    config = json.load(file)

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='~', intents=intents)

client.remove_command("help")


@client.event
async def on_ready():
    print("ready to serve!")

    for filename in listdir('./cogs'):
        if filename.endswith('.py') and filename != '__init__.py':
            await client.load_extension(f'cogs.{filename[:-3]}')


client.run(config["secrets"]["token"])

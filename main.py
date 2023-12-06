from discord.ext import commands
from os import listdir

import discord
import json
import wavelink

import utils
from modules.message import MessageModule

music_disabled = False

with open("config.json", "r") as file:
    config = json.load(file)

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='~', intents=intents, owner_id=config["owner_id"])

client.remove_command("help")

@client.event
async def on_command_error(ctx, err):
    print(err)
    if isinstance(err, commands.BadArgument):
        await ctx.send(f"```{err}```")
    elif isinstance(err, commands.MissingRequiredArgument):
        await ctx.send(f"```{err}```")
    elif isinstance(err, commands.NotOwner):
        return


@client.event
async def on_ready():
    print("ready to serve!")
    await init_lavalink()


@client.event
async def on_message(message: discord.Message):
    message_handler = MessageModule(message)
    await message_handler.init_gif()
    await client.process_commands(message)


async def init_lavalink():
    node1 = wavelink.Node(uri='http://n1.proxied.host:25589', password='wayvlink')
    await wavelink.Pool.connect(client=client, nodes=[node1])

    for filename in listdir('./cogs'):
        if filename.endswith('.py') and filename != '__init__.py':
            await client.load_extension(f'cogs.{filename[:-3]}')


client.run(config["secrets"]["token"])

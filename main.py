from discord.ext import commands
from os import listdir

import discord
import json
import wavelink
import gd

import utils

music_disabled = False

channels = {
    "daily": 1111472635520487474,
    "weekly": 1111472730781532211
}

with open("config.json", "r") as file:
    config = json.load(file)

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='~', intents=intents)
gd_client = gd.Client()

#client.remove_command("help")


@gd_client.event
async def on_daily(daily: gd.Level):
    channel = client.get_channel(channels["daily"])
    if channel.type == discord.ChannelType.text:
        await channel.send(embed=utils.create_level_embed(level=daily))


@client.event
async def on_command_error(ctx, err):
    if isinstance(err, commands.BadArgument):
        await ctx.send(f"```{err}```")
    elif isinstance(err, commands.MissingRequiredArgument):
        await ctx.send(f"```{err}```")


@client.event
async def on_ready():
    print("ready to serve!")

    node1 = wavelink.Node(uri='http://n1.proxied.host:25506', password='proxied.host')
    await wavelink.NodePool.connect(client=client, nodes=[node1])

    for filename in listdir('./cogs'):
        if filename.endswith('.py') and filename != '__init__.py':
            await client.load_extension(f'cogs.{filename[:-3]}')


client.run(config["secrets"]["token"])

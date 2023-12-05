import discord
from discord.ext import commands
# import gd
import json


# def create_level_embed(level: gd.Level):
#     embed = discord.Embed(title=f"{level.name} ({level.creator})", description=level.description)
#    embed.add_field(name="coins", value=level.coins, inline=True)
#    embed.add_field(name="Length", value=level.length, inline=True)
#    embed.add_field(name="Difficulty", value=level.difficulty, inline=True)
#    embed.add_field(name="Song", value=level.song, inline=True)
#    return embed


def get_config():
    with open("config.json", "r") as file:
        return json.load(file)


def is_owner(ctx: commands.Context):
    config = get_config()
    return ctx.author.id == config['owner_id']


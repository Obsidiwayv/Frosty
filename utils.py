from discord.ext import commands
import json


def get_config():
    with open("config.json", "r") as file:
        return json.load(file)


def is_owner(ctx: commands.Context):
    config = get_config()
    return ctx.author.id == config['owner_id']

#  Copyright (c) 2024
#
#  This file is part of Octane. belonging to Horizon and Wayvshock (Obsidiwayv)
#
#  No part of Octane, including this file, may be copied, modified, propagated, or distributed.

from discord.ext import commands
from os import listdir

import discord
import json
import wavelink

import logger
import helpers.mysql

music_disabled = False
database = helpers.mysql.MySQLHelper()


def main():
    with open("config.json", "r") as file:
        config = json.load(file)

    intents = discord.Intents.default()
    intents.message_content = True

    client = commands.Bot(
        command_prefix='~',
        intents=intents,
        owner_id=config["owner_id"]
    )

    client.remove_command("help")

    @client.event
    async def on_command_error(ctx, err):
        print(err)
        if isinstance(err, commands.BadArgument):
            await ctx.send(f"You need {len(err.args)} for this command.")
        elif isinstance(err, commands.MissingRequiredArgument):
            await ctx.send(f"```{err.param} needs an argument.```")
        elif isinstance(err, commands.NotOwner):
            return

    @client.event
    async def on_ready():
        logger.log_info("Online!")
        await init_lavalink()
        await load()

    async def init_lavalink():
        node1 = wavelink.Node(uri='', password='wayvlink')
        await wavelink.Pool.connect(client=client, nodes=[node1])

    async def load():
        for filename in listdir('./cogs'):
            if filename.endswith('.py') and filename != '__init__.py':
                await client.load_extension(f'cogs.{filename[:-3]}')

    client.run(config["secrets"]["token"])


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())

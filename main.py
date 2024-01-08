import re

from discord.ext import commands
from os import listdir

import discord
import json
import wavelink

import dragon.gd.request_client
import dragon.gd.gd_decode
from dragon import logger
import helpers.mysql
from modules.message import MessageModule

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
            await ctx.send(f"```{err}```")
        elif isinstance(err, commands.MissingRequiredArgument):
            await ctx.send(f"```{err.param} needs an argument.```")
        elif isinstance(err, commands.NotOwner):
            return

    @client.event
    async def on_ready():
        # print("Clearing image cache...")
        # cache_directory = "cache"
        # for filename in os.listdir(cache_directory):
        #    file_path = os.path.join(cache_directory, filename)
        #    if os.path.isfile(file_path) and filename.lower().endswith(
        #            ('.png', '.jpg', '.jpeg', '.gif', '.mp4', 'mp3')):
        #        os.remove(file_path)
        logger.log_info("Online!")
        await init_lavalink()
        await load()

    @client.event
    async def on_message(message: discord.Message):
        message_handler = MessageModule(message)
        await message_handler.init_gif()
        await client.process_commands(message)

    @client.event
    async def on_message_delete(message: discord.Message):
        if message.author.id == config['owner_id']:
            return
        if re.compile(fr'<@!?{config['owner_id']}>').search(message.content):
            user = await client.fetch_user(config['owner_id'])
            pinged_content = f"content:\n```\n{message.content}\n```" if message.content else ""
            message_attr = {
                "content": f'you got pinged!\noffender: {message.author.name}\n{pinged_content}'
            }

            if message.attachments:
                files = [await attachment.to_file() for attachment in message.attachments]
                message_attr["files"] = files
            await user.send(**message_attr)

    async def init_lavalink():
        node1 = wavelink.Node(uri='http://n1.proxied.host:25589', password='wayvlink')
        await wavelink.Pool.connect(client=client, nodes=[node1])

    async def load():
        for filename in listdir('./cogs'):
            if filename.endswith('.py') and filename != '__init__.py':
                await client.load_extension(f'cogs.{filename[:-3]}')

    client.run(config["secrets"]["token"])


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())

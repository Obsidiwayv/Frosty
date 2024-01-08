import os
import typing
from datetime import date
from io import BytesIO
from time import sleep
from discord.ext import commands

import discord

import assets.images as assets
import dragon.logger
from utils import get_config


def sanitize_content(content):
    # Remove mentions from the content
    content = discord.utils.escape_mentions(content)
    return content


class Core(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config = get_config()
        self.sniped_messages = {}

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        dragon.logger.log_user(message)
        files = False
        if len(message.attachments) > 0:
            # There are attachments in the message
            attachments = [await attachment.to_file() for attachment in message.attachments]
            files = await (self.bot.get_channel(self.config["channels"]["attachments"])
                           .send(content=f"{message.author.id} - {date.today()}", files=attachments))

        self.sniped_messages[message.channel.id] = (
            message.content,
            message.author,
            message.created_at,
            files
        )

    @commands.command()
    async def ping(self, ctx: commands.Context):
        await ctx.send(content=f"Pong! {self.bot.latency}")

    @commands.command()
    async def botinfo(self, ctx: commands.Context):
        embed = discord.Embed(color=0x00FF7F)
        embed.description = "A fluffy protogen to serve!"
        embed.set_image(url="https://wayvlyte.space/octane_banner.png")
        embed.add_field(name="developer", value="obsidiwayv/obsidiwayv#3420", inline=True)
        embed.add_field(name="Protogen software version", value="1.4.0-Thorium", inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    async def destruct(self, ctx: commands.Context):
        await ctx.message.delete()
        await ctx.send("Im going to commit tnt")
        await ctx.send("in 3")
        sleep(3)
        await ctx.send("2")
        sleep(3)
        await ctx.send("1")
        sleep(5)
        await ctx.send("Just kidding ( ͡° ͜ʖ ͡°)")

    @commands.command()
    async def emojis(self, ctx: commands.Context):
        available = []
        for emoji in self.bot.emojis:
            available.append(emoji.name)

        print(available)
        await ctx.send(content=f"```bots available emojis```\n{available}")

    @staticmethod
    async def snipe_message(ctx, message_info):
        message_content, message_author, message_time, bot_message = message_info
        msg_attr = {
            "content": f"{sanitize_content(message_content)}\n\n{message_author}"
        }

        if bot_message:
            msg_attr["files"] = [await attachment.to_file() for attachment in bot_message.attachments]

        await ctx.send(**msg_attr)
        return

    @commands.command(aliases=["q", "s", "sq", "snipe"])
    async def quote(
            self,
            ctx: commands.Context,
            channel: typing.Optional[discord.TextChannel] = None,
            message_id: typing.Optional[int] = 0
    ):
        channel = channel or ctx.channel
        channel_id = channel.id

        if message_id != 0:
            # Quote the specified message
            try:
                if channel:
                    channel = ctx.guild.get_channel(
                        channel_id if not isinstance(channel, discord.TextChannel) else channel.id)
                    if not channel:
                        print("Couldn't find the channel")
                        await ctx.message.add_reaction(self.config["emotes"]["no"])
                        return
                else:
                    channel = ctx.channel

                message = await channel.fetch_message(message_id)
            except discord.NotFound:
                print("Not found")
                await ctx.message.add_reaction(self.config["emotes"]["no"])

            if not ctx.author.id == self.config["owner_id"]:
                if message.author.id == self.config["owner_id"]:
                    return

            has_content = False

            message_attr = {
                "allowed_mentions": discord.AllowedMentions(
                    everyone=False,
                    users=True,
                    roles=False,
                    replied_user=True
                )
            }

            if ctx.message.reference:
                message_attr["reference"] = ctx.message.reference

            if message.content:
                has_content = True
                message_attr['content'] = f'"{message.content}"\n\\- {message.author.name} probably'

            if message.attachments:
                files = [await attachment.to_file() for attachment in message.attachments]
                message_attr["files"] = files

            await ctx.send(**message_attr)
            if not has_content:
                await ctx.send(f'\\- {message.author.name} probably')
        else:
            message_info = self.sniped_messages.get(channel_id)
            if message_info:
                message_content, message_author, message_time, attachments = message_info
                if not ctx.author.id == self.config["owner_id"]:
                    if message_author.id == self.config["owner_id"]:
                        return
                await self.snipe_message(ctx, message_info)
                return
            else:
                await ctx.send("No recently deleted messages found in the specified channel.")

            # Check for mentions and snipe the most recent message from the mentioned channel
            if ctx.message.channel_mentions:
                mentioned_channel = ctx.message.channel_mentions[0]
                mentioned_channel_id = mentioned_channel.id

                # Fetch the most recent deleted message from the mentioned channel
                message_info = self.sniped_messages.get(mentioned_channel_id)
                if message_info:
                    message_content, message_author, message_time, attachments = message_info
                    if not ctx.author.id == self.config["owner_id"]:
                        if message_author.id == self.config["owner_id"]:
                            return
                    await self.snipe_message(ctx, message_info)
                    return
                else:
                    await ctx.send(f"No recently deleted messages found in {mentioned_channel.mention}.")

    @commands.command()
    async def card(self, ctx: commands.Context):
        ts = 180
        image_path = await assets.draw_song_interface(
            "payload.track.title",
            400000,
            "payload.track.author",
            (ts, ts),
            "https://wayvlyte.space/backgrounds/Crimson.jpg"
        )
        with open(image_path, 'rb') as file:
            # Create a discord.File object
            modern_interface_image = discord.File(BytesIO(file.read()), filename=f"cover_test.png")

            # Send the image to the Discord channel
            await ctx.send(file=modern_interface_image)


async def setup(bot: commands.Bot):
    await bot.add_cog(Core(bot))

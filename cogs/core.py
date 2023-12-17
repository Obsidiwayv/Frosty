import typing
from io import BytesIO
from time import sleep
from discord.ext import commands

import discord

import assets.images as assets
from utils import get_config


class Core(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config = get_config()

    @commands.command()
    async def ping(self, ctx: commands.Context):
        await ctx.send(content=f"Pong! {self.bot.latency}")

    @commands.command()
    async def botinfo(self, ctx: commands.Context):
        embed = discord.Embed(color=0x00FF7F)
        embed.description = "A fluffy protogen to serve!"
        embed.set_image(url="https://wayvlyte.space/octane_banner.png")
        embed.add_field(name="developer", value="obsidiwayv/obsidiwayv#3420", inline=True)
        embed.add_field(name="Protogen software version", value="1.2.0-Titanium", inline=True)
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

    @commands.command(aliases=["q"])
    async def quote(
            self,
            ctx: commands.Context,
            channel_id: int | discord.TextChannel,
            message_id: typing.Optional[int] = 0
    ):
        message: discord.Message
        try:
            if not message_id == 0:
                channel = ctx.guild.get_channel(
                    channel_id if not isinstance(channel_id, discord.TextChannel) else channel_id.id
                )
                if not channel:
                    print("Couldn't find the channel")
                    await ctx.message.add_reaction(self.config["emotes"]["no"])
                    return
                message = await channel.fetch_message(message_id)
            else:
                message = await ctx.channel.fetch_message(channel_id)
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

        if message.embeds:
            message_attr["embeds"] = message.embeds

        if message.content:
            has_content = True
            message_attr['content'] = f'"{message.content}"\n\\- {message.author.name} probably'

        if message.attachments:
            files = [await attachment.to_file() for attachment in message.attachments]
            message_attr["files"] = files

        await ctx.send(**message_attr)
        if not has_content:
            await ctx.send(f'\\- {message.author.name} probably')

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

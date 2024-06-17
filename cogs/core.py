#  Copyright (c) 2024
#
#  This file is part of Octane. belonging to Horizon and Wayvshock (Obsidiwayv)
#
#  No part of Octane, including this file, may be copied, modified, propagated, or distributed.

from datetime import date
from io import BytesIO
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
        embed.add_field(name="Protogen software version", value="1.4.0-Thorium", inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
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

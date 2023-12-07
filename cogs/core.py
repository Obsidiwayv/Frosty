from io import BytesIO
from time import sleep
from discord.ext import commands

import discord

import assets.images as assets


class Core(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

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

from os import getcwd
from time import sleep

from discord.ext import commands

import discord


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
        embed.add_field(name="Protogen software version", value="1.2-Nexus", inline=True)
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


async def setup(bot: commands.Bot):
    await bot.add_cog(Core(bot))

from discord.ext import commands

import discord


class GD(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: commands.Context):
        await ctx.send(content=f"Pong! {self.bot.latency}")


async def setup(bot: commands.Bot):
    await bot.add_cog(GD(bot))

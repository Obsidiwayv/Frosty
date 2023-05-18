from discord.ext import commands

import discord
import wavelink


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

#    @commands.command()
#    async def play(self, ctx: commands.Context, *, query: str):


async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))

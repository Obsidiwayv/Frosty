from discord.ext import commands

import discord


class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

# TODO: make music commands here
#    @commands.command()
#    async def search(self, ctx: commands.Context):


async def setup(bot: commands.Bot):
    await bot.add_cog(Fun(bot))

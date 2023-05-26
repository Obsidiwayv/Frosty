from discord.ext import commands

import discord
import gd

import utils

client = gd.Client()
config = utils.get_config()


class GD(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def search(self, ctx: commands.Context, *, level_name):
        context = ""
        levels = await client.search_levels(query=level_name, pages=[1])
        for level in levels:
            context += f"{level.name} ({level.id}) - {level.creator}\n"
        await ctx.send(content=f"```{context}```")

    @commands.command()
    async def level(self, ctx: commands.Context, level_id: int):
        level = await client.get_level(level_id)
        await ctx.send(embed=utils.create_level_embed(level=level))

    @commands.command()
    async def daily(self, ctx: commands.Context):
        level = await client.get_daily()
        await ctx.send(embed=utils.create_level_embed(level=level))



async def setup(bot: commands.Bot):
    await bot.add_cog(GD(bot))

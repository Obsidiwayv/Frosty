#  Copyright (c)
#
#  This file is part of Octane. belonging to Horizon and Wayvshock (Obsidiwayv)
#
#  No part of Octane, including this file, may be copied, modified, propagated, or distributed.

import random

from discord.ext import commands
from redditmemeapi import specifysub

import discord


async def generate_post_from_reddit(sub: str):
    subreddit = specifysub(sub)
    danks = random.choice(subreddit)
    embed = discord.Embed(color=0x703BE7)
    embed.description = danks['title']
    embed.set_footer(text=danks['author'])
    embed.set_image(url=danks['img_url'])
    return embed


class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def meme(self, ctx: commands.Context):
        await ctx.send(embed=await generate_post_from_reddit("dankmemes"))

    @commands.command()
    async def proto(self, ctx: commands.Context):
        await ctx.send(embed=await generate_post_from_reddit("protogen"))

    @commands.command()
    async def furry(self, ctx: commands.Context):
        await ctx.send(embed=await generate_post_from_reddit("furry_irl"))


async def setup(bot: commands.Bot):
    await bot.add_cog(Fun(bot))

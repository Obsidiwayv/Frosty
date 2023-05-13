from discord.ext import commands
from memelib.api import DankMemeClient

import discord

memes = DankMemeClient()


class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def meme(self, ctx: commands.Context):
        danks = await memes.async_meme(subreddit="dankmemes")
        embed = discord.Embed(color=0x703BE7)
        embed.description = f"{danks['title']} | {danks['author']}"
        embed.set_image(url=danks['img_url'])
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Fun(bot))

import discord
import requests
import colour

from discord.ext import commands
from bs4 import BeautifulSoup
from requests_html import AsyncHTMLSession


class Colours(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.pantone_url = "https://connect.pantone.com/picker/#"

    async def get_pantone_color(self):
        session = AsyncHTMLSession()
        res = await session.get(self.pantone_url)
        await res.html.arender()
        print(res.text)

    @commands.command()
    async def pantone(self, ctx: commands.Context, colour: str):
        await self.get_pantone_color()

    @commands.group()
    async def colour_command(self, ctx: commands.Context):
        if not ctx.invoked_subcommand:
            pass

    @colour_command.command()
    async def convert(self, ctx: commands.Context, hex: str):
        rgb = colour.hex2rgb(hex)
        web = colour.hex2web(hex)



async def setup(bot: commands.Bot):
    await bot.add_cog(Colours(bot))

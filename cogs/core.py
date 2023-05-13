from os import getcwd

from discord.ext import commands

import discord


class Core(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: commands.Context):
        await ctx.send(content=f"Pong! {self.bot.latency}")

    @commands.command()
    async def info(self, ctx: commands.Context):
        embed = discord.Embed(color=0x703BE7)
        frosty = discord.File(f"{getcwd()}/img/Frosty_Banner.png", filename="image.png")
        embed.description = "A fluffy protogen to serve!"
        embed.set_image(url="attachment://image.png")
        embed.add_field(name="developer", value="Obisidiwayv#3420 (tag may subject to change)", inline=True)
        embed.add_field(name="Protogen software version", value="1.0-Nexus", inline=True)
        await ctx.send(embed=embed, file=frosty)

    @commands.command()
    async def help(self, ctx: commands.Context):
        embed = discord.Embed(color=0x703BE7)
        frosty = discord.File(f"{getcwd()}/img/Frosty_Banner.png", filename="image.png")
        embed.set_image(url="attachment://image.png")
        embed.add_field(name="Core Commands", value="info, ping")
        embed.add_field(name="Fun Commands", value="meme")
        embed.add_field(name="Minecraft Server", value="status")
        embed.set_footer(text="Default prefix is ~")
        await ctx.send(embed=embed, file=frosty)


async def setup(bot: commands.Bot):
    await bot.add_cog(Core(bot))

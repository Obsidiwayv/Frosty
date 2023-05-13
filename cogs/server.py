from discord.ext import commands
from pydactyl import PterodactylClient

import discord

py = PterodactylClient("https://proxied.host/", "ptlc_cSGpz27CvZpeWLIIiJdnQLwiwIyvjbPXVcrYQABGyBi")


class Server(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def status(self, ctx: commands.Context):
        information = py.client.servers.get_server("f1969fd7-a816-4125-a455-5b3e1cde16d3")

        address = information['sftp_details']['ip']
        port = information['sftp_details']['port']

        embed = discord.Embed(color=0x703BE7)
        embed.description = "Minecraft server information for Project Winter"
        embed.add_field(name="Server Address", value=f"{address}:{port}", inline=True)
        embed.add_field(name="Minecraft Version", value="1.18.2", inline=True)
        embed.add_field(name="Java Version", value=information['docker_image'], inline=True)
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Server(bot))

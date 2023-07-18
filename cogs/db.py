from discord.ext import commands

import discord

import helpers.mysql
import utils


class DB(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = helpers.mysql.MySQLHelper()

    @commands.command()
    async def dbping(self, ctx: commands.Context):
        await ctx.send(content=f"Here you are: {self.db.ping_db()}")

    @commands.command()
    async def dbitem(self, ctx: commands.Context, item: str):
        if utils.is_owner(ctx):
            with self.db.database:
                with self.db.database.cursor() as cursor:
                    sql = "SELECT * FROM `ShopItem` WHERE `name`=%s"
                    cursor.execute(sql, (item))
                    result = cursor.fetchone()
                    return await ctx.send(content=f"```\n{result}\n```")


async def setup(bot: commands.Bot):
    await bot.add_cog(DB(bot))

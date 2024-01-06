from discord.ext import commands

import utils
from main import database

import discord


class Tag(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = database
        self.config = utils.get_config()

    @staticmethod
    def get_tag_from_db(cursor, name: str, guild: int):
        sql = "SELECT `text`, `name`, `user` FROM `TAGS` WHERE `name`=%s AND `guild`=%s"
        cursor.execute(sql, (name, guild,))
        return cursor.fetchone()

    @commands.group(name="tag", invoke_without_command=True)
    async def tag(self, ctx: commands.Context, tag: str):
        with self.db.database_octane.cursor() as cursor:
            result = self.get_tag_from_db(cursor, tag, ctx.guild.id)
            if result:
                await ctx.send(result['text'])
            else:
                await ctx.send("There was no tag by that name.")
            cursor.close()

    @tag.command(aliases=["del"])
    async def delete(self, ctx: commands.Context, name: str):
        with self.db.database_octane.cursor() as cursor:
            data = self.get_tag_from_db(cursor, name, ctx.guild.id)

            if not data:
                await ctx.send("Tag doesn't exist.")

            if ctx.author.id in self.config["bot_admins"]:
                pass
            else:
                if not data['user'] == ctx.author.id:
                    if ctx.message.author.guild_permissions.administrator():
                        pass
                    else:
                        await ctx.send("That tag does not belong to you.")
                        return

            sql = "DELETE FROM `TAGS` WHERE `name`=%s AND `guild`=%s"

            try:
                cursor.execute(sql, (name, ctx.guild.id,))
                await ctx.send(f"Deleted tag `{name}`")
            except Exception as e:
                await ctx.send("Unable to delete your tag.")

    @tag.command(aliases=["list"])
    async def all(self, ctx: commands.Context):
        with self.db.database_octane.cursor() as cursor:
            sql = "SELECT `text`, `name`, `user` FROM `TAGS` WHERE `guild`=%s"
            cursor.execute(sql, (ctx.guild.id,))
            result = cursor.fetchall()
            tags = ""
            for t in result:
                tags += f"{t['name']}, "

            await ctx.send(f"```\n{tags}\n```")
            cursor.close()

    @tag.command(aliases=["who"])
    async def info(self, ctx: commands.Context, tag: str):
        with self.db.database_octane.cursor() as cursor:
            result = self.get_tag_from_db(cursor, tag, ctx.guild.id)

            if not result:
                await ctx.send("That tag doesn't appear to exist.")
                return

            await ctx.send(
                content=f"Belongs to: `{result['user']}` <@{result['user']}>",
                allowed_mentions=discord.AllowedMentions(users=False)
            )
            cursor.close()

    @tag.command(aliases=["add"])
    async def create(self, ctx: commands.Context, name: str, *, txt: str):
        if len(name) > 15:
            await ctx.send("Tag name cannot go beyond 15.")
            return
        elif len(txt) > 2000:
            await ctx.send("Tag text cannot exceed 2000 characters.")
            return
        with self.db.database_octane.cursor() as cursor:
            try:
                old_data = self.get_tag_from_db(cursor, name, ctx.guild.id)
                if old_data:
                    if name.lower() == old_data["name"].lower():
                        await ctx.send("2 Tags cannot have the same name.")
                        return

                sql = "INSERT INTO `TAGS` (`guild`, `user`, `name`, `text`) VALUES (%s, %s, %s, %s)"

                print(ctx.guild.id, ctx.message.author.id, name, txt)
                cursor.execute(sql, (ctx.guild.id, ctx.message.author.id, name, txt))
                self.db.database_octane.commit()
                await ctx.send(f"created `{name}`")
            except Exception as e:
                await ctx.send(f"I could not save your tag.\n```\n{e}\n```")
                return
            finally:
                cursor.close()


async def setup(bot: commands.Bot):
    await bot.add_cog(Tag(bot))

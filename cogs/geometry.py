import os
import urllib.parse
from io import BytesIO

from PIL import Image
from discord.ext import commands

import discord

import dragon.gd.request_client
import dragon.gd.gd_decode
# import gd

import utils

# client = gd.Client()
config = utils.get_config()


class GD(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @staticmethod
    def render_difficulty_face(diff: str, featured: bool, epic: bool):
        difficulty_face = Image.new("RGBA", (180, 180), (0, 0, 0, 0))
        difficulty_face.convert("RGBA")

        face_type = "default"

        directory = "assets/geometrydash"

        face = Image.open(f"{directory}/{diff}.png")

        image = None

        if featured and epic:
            image = Image.alpha_composite(Image.open(f"{directory}/Epic.png").convert("RGBA"), face)
            face_type = "epic"
        elif featured:
            image = Image.alpha_composite(Image.open(f"{directory}/Featured.png").convert("RGBA"), face)
            face_type = "featured"
        elif epic:
            image = Image.alpha_composite(Image.open(f"{directory}/Epic.png").convert("RGBA"), face)
            face_type = "epic"
        else:
            difficulty_face.paste(face)

        # Save the image to a temporary file
        image_path = os.path.join("assets", "rendered", f"face_{diff.lower()}_{face_type}.png")
        if featured:
            image.save(image_path)
        elif epic:
            image.save(image_path)
        elif featured and epic:
            image.save(image_path)
        else:
            difficulty_face.save(image_path)

        return image_path

    @commands.command()
    async def search(self, ctx: commands.Context, level_name: str):
        try:
            fields = ""
            result = dragon.gd.request_client.make("getGJLevels21", {
                "str": level_name,
                "total": 10,
                "type": 0
            })
            levels = dragon.gd.gd_decode.level_data(result.text)
            fields += f"## Search: `{level_name}`\n"
            fields += "```\n"

            if not len(levels):
                await ctx.send("There are no levels here...")
                return

            for level in levels:
                fields += f"{level["id"]} - {level["name"]} by {level["creator"]} ({level["difficulty"]})\n\n"

            fields += "```"
            fields += f"{len(levels)} out of 10 results"

            await ctx.send(fields)
        except Exception as e:
            await ctx.send(f"ERROR\b```\n{e}\n```")

    @commands.command()
    async def level(self, ctx: commands.Context, level_id: int):
        try:
            request = dragon.gd.request_client.make("getGJLevels21", {
                "str": str(level_id),
                "type": 0
            })
            levels = dragon.gd.gd_decode.level_data(request.text)
            if len(levels) == 0:
                await ctx.send("That level doesn't appear to exist...")
                return
            level = levels[0]
            embed = discord.Embed()

            embed.title = str(level["id"])
            embed.description = f"{level["name"]} by {level["creator"]}\n```{level["description"]}```"

            image_path = self.render_difficulty_face(
                level["difficulty"],
                level["featured"],
                level["epic"]
            )

            embed.add_field(
                name="Data",
                value=(
                    f"Stars: {level['stars']}\n"
                    f"Length: {level['length']}\n"
                    f"Coins: {level['coins']}\n"
                    f"Objects: {level['objects']}\n"
                    f"Likes: {level['likes']}"
                )
            )

            embed.add_field(
                name="Song",
                value=f"({level['song']['file_size'] if level['song'].get("file_size") else "Official Song"})  "
                      f"{level['song']['artist']} - "
                      f"{level['song']['name']}"
            )

            embed.add_field(
                name="Song File",
                value=urllib.parse.unquote(level['song']['link']),
                inline=False
            )

            with open(image_path, 'rb') as file:
                embed.set_thumbnail(url=f"attachment://{image_path.split("\\")[2]}")
                await ctx.send(
                    content=f"Creator - {level['creator']}",
                    embed=embed,
                    file=discord.File(image_path, filename=image_path.split("\\")[2])
                )
        except Exception as e:
            await ctx.send(f"ERROR\n```\n{e}\n```")

    @commands.command()
    async def more(self, ctx: commands.Context):
        await ctx.send("Want more geometry dash content? invite robtop 2! coming soon:tm:")


async def setup(bot: commands.Bot):
    await bot.add_cog(GD(bot))

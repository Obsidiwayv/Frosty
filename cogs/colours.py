import colour
import helpers.colour_convert as colour_converter

from discord.ext import commands


class Colours(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group()
    async def colour(self, ctx: commands.Context):
        if not ctx.invoked_subcommand:
            pass

    @colour.command()
    async def to_rgb(self, ctx: commands.Context, hex_arg: str):
        try:
            rgb = colour.hex2rgb(hex_arg)
            await ctx.send(f"input: `{hex_arg}` output: `{rgb}`")
        except ValueError:
            await ctx.send("Argument provided is not a hexadecimal string.")

    @colour.command()
    async def to_web(self, ctx: commands.Context, hex_arg: str):
        try:
            web = colour.hex2web(hex_arg)
            await ctx.send(f"input: `{hex_arg}` output: `{web}`")
        except ValueError:
            await ctx.send("Argument provided is not a hexadecimal string.")

    @colour.command(aliases=["con"])
    async def convert(self, ctx: commands.Context, color_arg: str):
        try:
            converter = colour_converter.ColorConverter(color_arg)
            formats = converter.convert_formats()
            formatted_text = "{\n"
            for key, value in formats.items():
                formatted_text += f"    {key}: {value},\n"
            formatted_text += "}"
            await ctx.send(f"input: `{color_arg}`, output:\n```\n{formatted_text}\n```")
        except ValueError:
            await ctx.send("color_arg wasn't a hexadecimal.")


async def setup(bot: commands.Bot):
    await bot.add_cog(Colours(bot))

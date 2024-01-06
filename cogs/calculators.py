import math
import typing

from discord.ext import commands


class ShapeType:
    def __init__(self, shape_type: str):
        self.shape_type = shape_type

    def is_3d(self):
        return self.shape_type == "3D"

    def is_2d(self):
        return self.shape_type == "2D"


class Shapes:
    @staticmethod
    def calculate_triangle_vertices_3d(side_length):
        vertices = [(0, 0, 0), (side_length, 0, 0), (side_length / 2, (3 ** 0.5 / 2) * side_length, 0)]
        return vertices

    @staticmethod
    def calculate_square_vertices_3d(side_length):
        vertices = [(0, 0, 0), (side_length, 0, 0), (side_length, side_length, 0), (0, side_length, 0)]
        return vertices

    @staticmethod
    def calculate_cylinder_vertices_3d(radius, height, num_segments=16):
        vertices = []
        for i in range(num_segments):
            theta = 2 * math.pi * i / num_segments
            x = radius * math.cos(theta)
            y = radius * math.sin(theta)
            vertices.append((x, y, 0))
            vertices.append((x, y, height))
        return vertices

    @staticmethod
    def calculate_triangle_vertices_2d(side_length):
        vertices = [(0, 0), (side_length, 0), (side_length / 2, (3 ** 0.5 / 2) * side_length)]
        return vertices

    @staticmethod
    def calculate_square_vertices_2d(side_length):
        vertices = [(0, 0), (side_length, 0), (side_length, side_length), (0, side_length)]
        return vertices


class Calculators(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def triangle(self, ctx: commands.Context, side_lengths: int, st: str):
        shape = ShapeType(st)
        shape_vert = Shapes()

        if shape.is_3d():
            await ctx.send(f"Vertices for 3D Triangle: `{shape_vert.calculate_triangle_vertices_3d(side_lengths)}`")
        else:
            await ctx.send(f"Vertices for 2D Triangle: `{shape_vert.calculate_triangle_vertices_2d(side_lengths)}`")

    @commands.command()
    async def square(self, ctx: commands.Context, side_lengths: int, st: str):
        shape = ShapeType(st)
        shape_vert = Shapes()

        if shape.is_3d():
            await ctx.send(f"Vertices for 3D Square: `{shape_vert.calculate_square_vertices_3d(side_lengths)}`")
        else:
            await ctx.send(f"Vertices for 2D Square: `{shape_vert.calculate_square_vertices_2d(side_lengths)}`")

    @commands.command()
    async def piston(self, ctx: commands.Context, radius: int, height: int, segments: typing.Optional[int] = 16):
        shapes = Shapes()

        await ctx.send(f"output:```\n{shapes.calculate_cylinder_vertices_3d(radius, height, segments)}\n```")


async def setup(bot: commands.Bot):
    await bot.add_cog(Calculators(bot))

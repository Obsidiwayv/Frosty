from discord.ext import commands

import ossapi
import discord


class Osu(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.osu = ossapi.Ossapi(28670, "w48eJvyRFVcupuAiYPKPvxgVJnfiynD3rnugtHXr")

    @commands.group()
    async def osu(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send("I can't seem to find that subcommand")

    @osu.command()
    async def player(self, ctx: commands.Context, *, player_name: str):
        player: ossapi.User = self.osu.user(player_name)
        if not player:
            await ctx.send("No player name by that username")
            return

        profile_url = "https://osu.ppy.sh/users"
        highest_rank = 'none' if not player.rank_highest else player.rank_highest.rank

        player_embed = discord.Embed()

        player_embed.colour = discord.Colour.magenta() if not player.profile_colour \
            else discord.Colour.from_str(player.profile_colour)

        player_embed.title = player.username
        player_embed.description = f"This users highest rank is {highest_rank}"
        player_embed.add_field(name="ID", value=str(player.id), inline=True)
        player_embed.add_field(name="active", value="no" if not player.is_active else "yes", inline=True)

        player_embed.set_thumbnail(url=player.avatar_url)

        await ctx.send(content=f"{profile_url}/{player.id}", embed=player_embed)

    @osu.command()
    async def map(self, ctx: commands.Context, *, map_name: int):
        try:
            beatmap: ossapi.Beatmap = self.osu.beatmap(map_name)
        except ValueError:
            await ctx.send("Cannot find a beatmap by that id!")
            return

        beatmap_embed = discord.Embed()

        beatmap_embed.add_field(name="Beatmap Owner",
                                value="no owner" if not hasattr(beatmap.owner, "username") else beatmap.owner.username,
                                inline=True)
        beatmap_embed.add_field(name="BPM",
                                value=beatmap.bpm,
                                inline=True)
        beatmap_embed.add_field(name="Circles",
                                value=beatmap.count_circles,
                                inline=True)
        beatmap_embed.add_field(name="Sliders",
                                value=beatmap.count_sliders,
                                inline=True)
        beatmap_embed.add_field(name="Spinners",
                                value=beatmap.count_spinners,
                                inline=True)
        beatmap_embed.add_field(name="Last Updated",
                                value=beatmap.last_updated,
                                inline=True)
        beatmap_embed.add_field(name="Is Scoreable?",
                                value="no" if not beatmap.is_scoreable else "yes",
                                inline=True)
        beatmap_embed.colour = discord.Colour.magenta()

        await ctx.send(embed=beatmap_embed, content=beatmap.url)


async def setup(bot: commands.Bot):
    await bot.add_cog(Osu(bot))

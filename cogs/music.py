from discord.ext import commands

import discord
import wavelink

voice_ids = {}


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def play(self, ctx: commands.Context, *, query: str):
        if not ctx.voice_client:
            await ctx.send("When the bot joins it will be deafened")
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = ctx.voice_client

        track = await wavelink.YouTubeTrack.search(query, return_first=True)
        await ctx.send(f"```Now Playing {track.title}```\n{track.uri}")

        if not voice_ids.:
            voice_ids.update(f"{ctx.guild.id}", [track.title])
        else:
            voice_ids[f"{ctx.guild.id}"].append(track.title)

        print(voice_ids)

        while voice_ids[ctx.guild.id].count():
            if not vc.is_playing():
                first = voice_ids[f"{ctx.guild.id}"].pop()
                return await ctx.invoke(self.bot.get_command("play"), ctx=ctx, query=first)
        await vc.play(track)
        await ctx.guild.change_voice_state(channel=vc.channel, self_mute=False, self_deaf=True)

    @commands.command()
    async def disconnect(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client
        await vc.disconnect()


async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))

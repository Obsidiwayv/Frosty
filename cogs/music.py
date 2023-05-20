from discord.ext import commands

import discord
import wavelink

voice_ids = {}


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

#    @commands.Cog.listener()
#    async def on_wavelink_track_end(self, player: wavelink.Player):
#        if len(voice_ids[f"{player.guild.id}"]):
#            first = voice_ids[f"{player.guild.id}"].pop()
#            track = await wavelink.YouTubeTrack.search(first, return_first=True)
#            await player.play(track)

    @commands.command()
    async def play(self, ctx: commands.Context, *, query: str):
        if not ctx.voice_client:
            await ctx.send("When the bot joins it will be deafened")
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = ctx.voice_client

        track = await wavelink.YouTubeTrack.search(query, return_first=True)

        voice_ids[f"{ctx.guild.id}"] = []
        voice_ids[f"{ctx.guild.id}"].append(track.title)

        if len(voice_ids[f"{ctx.guild.id}"]) == 1:
            print(voice_ids, len(voice_ids[f"{ctx.guild.id}"]))
            await ctx.send(f"```Now Playing {track.title}```\n{track.uri}")
            await vc.play(track)
            await ctx.guild.change_voice_state(channel=vc.channel, self_mute=False, self_deaf=True)
        else:
            voice_ids[f"{ctx.guild.id}"].append(track.title)
            await ctx.send(f"Added {track.title} to the queue!")

    @commands.command()
    async def disconnect(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client
        await vc.disconnect()


async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))

from typing import cast

from discord.ext import commands

import discord
import wavelink

voice_ids = {}


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_wavelink_track_start(self, payload: wavelink.TrackStartEventPayload):
        started_embed = discord.Embed()
        started_embed.description = f"Started playing [{payload.track.title}]({payload.track.uri})"
        started_embed.set_image(url=payload.track.artwork)
        await payload.player.context.send(embed=started_embed)

    @commands.command()
    async def play(self, ctx: commands.Context, *, query: str):
        player: wavelink.Player
        player = cast(wavelink.Player, ctx.voice_client)

        if not player:
            try:
                player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
            except AttributeError:
                await ctx.send("oh no there is no channel for me to join")
                return

        tracks = await wavelink.Playable.search(query)

        player.autoplay = wavelink.AutoPlayMode.partial
        player.queue.mode = wavelink.QueueMode.normal
        if not hasattr(player, "context"):
            player.context = ctx

        songs: int | wavelink.Playable
        if isinstance(tracks, wavelink.Playlist):
            songs = await player.queue.put_wait(tracks)
        else:
            songs = await player.queue.put_wait(tracks[0])

        if not player.playing:
            track = player.queue.get()
            await player.play(track)
            await ctx.guild.change_voice_state(channel=player.channel, self_mute=False, self_deaf=True)
        else:
            added_embed = discord.Embed()
            if isinstance(tracks, wavelink.Playlist):
                added_embed.description = f"Added {songs} to the queue"
            else:
                song_name: str
                added_embed.description = f"Added {songs.title} to the queue"

            await ctx.send(embed=added_embed)

    @commands.command()
    async def disconnect(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client
        await vc.disconnect()

    @commands.command()
    async def queue(self, ctx: commands.Context):
        player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        if not player:
            await ctx.send("Queue is not available as nothing is playing")
            return

        output = ""
        que = list(player.queue)
        que.reverse()
        ln = 10 if len(que) > 10 else len(que)
        for i in range(ln):
            track = que[i]
            output += f"{i + 1}: {track.title}\n"

        if len(que) > 10:
            output += f"... {len(que) - ln} in queue ..."

        await ctx.send(f"```\n{output}\n```")


async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))

from discord.ext import commands

import discord
import wavelink

voice_ids = {}


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, payload: wavelink.TrackEventPayload):
        if payload.reason == "FINISHED":
            try:
                track = payload.player.queue.pop()
                await payload.player.play(track)
                await payload.player.context.send(f"```Started playing {track.title}```\n{track.uri}")
            except wavelink.QueueEmpty:
                await payload.player.stop()
                await payload.player.context.send("End of queue, stopped playing...")
        if payload.reason == "STOPPED":
            await payload.player.stop()

    @commands.command()
    async def play(self, ctx: commands.Context, *, query: str):
        if not ctx.voice_client:
            await ctx.send("When the bot joins it will be deafened")
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = ctx.voice_client

        track = await wavelink.YouTubeTrack.search(query, return_first=True)

        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild.id)
        if not hasattr(player, "context"):
            player.context = ctx

        vc.queue.put(track)

        if not vc.is_playing():
            first = vc.queue.pop()
            await ctx.send(f"```Now Playing {first.title}```\n{first.uri}")
            await vc.play(first)
            await ctx.guild.change_voice_state(channel=vc.channel, self_mute=False, self_deaf=True)
        else:
            await ctx.send(f"Added {track.title} to the queue!")

    @commands.command()
    async def disconnect(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client
        await vc.disconnect()

    @commands.command()
    async def queue(self, ctx: commands.Context):
        if not ctx.voice_client:
            await ctx.send("Queue is not available as nothing is playing")
        else:
            player = wavelink.NodePool.get_node().get_player(ctx.guild.id)

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

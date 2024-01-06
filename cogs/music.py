import re
from io import BytesIO
from math import isnan
from typing import cast
from discord.ext import commands

import discord
import wavelink
import asyncio

from utils import get_config

import assets.images as assets

voice_ids = {}
default_response = "I'm not in any voice channel!"


async def check_and_send(ctx: commands.Context, message: str):
    player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
    if not player:
        await ctx.send(message)
        return False
    return player


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config = get_config()

    @commands.Cog.listener()
    async def on_wavelink_track_start(self, payload: wavelink.TrackStartEventPayload):
        ts = 180
        image_path = await assets.draw_song_interface(
            payload.track.title,
            payload.track.length,
            payload.track.author,
            (ts, ts),
            payload.track.artwork
        )
        with open(image_path, 'rb') as file:
            # Create a discord.File object
            modern_interface_image = discord.File(BytesIO(file.read()), filename=f"cover_{payload.track.title}.png")

            # Send the image to the Discord channel
            await payload.player.context.send(file=modern_interface_image)

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

        if not tracks:
            await ctx.send("No tracks by that name...")
            return

        has_choice = False
        choice_track = None

        player.autoplay = wavelink.AutoPlayMode.partial
        player.queue.mode = wavelink.QueueMode.normal
        if not hasattr(player, "context"):
            player.context = ctx

        if not isinstance(tracks, wavelink.Playlist):
            if len(tracks) != 1:
                songs_list = ""
                s = 0

                while s <= 14:
                    song_data = tracks[s]
                    songs_list += f"{s + 1}. {song_data.author} - {song_data.title}\n"
                    s += 1

                await ctx.send(f"```\n{songs_list}\n```\nsay a number 1 - 15 to pick a song")

                def check(m):
                    return m.author == ctx.author

                try:
                    waited = await self.bot.wait_for("message", timeout=25, check=check)
                    if not re.match(r'^\d+$', waited.content):
                        await ctx.send("The string you provided isn't a number!")
                        return
                    parsed_int = int(waited.content)

                    if isnan(parsed_int):
                        await ctx.send("The number you provided isn't a number!")
                        return

                    after_error_subtract = parsed_int - 1

                    if not tracks[after_error_subtract]:
                        await ctx.send("There is no track of that number")
                        return

                    await player.queue.put_wait(tracks[after_error_subtract])
                    choice_track = tracks[after_error_subtract]
                    has_choice = True
                except asyncio.TimeoutError:
                    await ctx.send('Canceled choice')
                    return

        songs: int
        if not has_choice:
            if isinstance(tracks, wavelink.Playlist):
                playlist = ""
                songs = await player.queue.put_wait(tracks)
                for track in tracks:
                    playlist += f"{track.author} - {track.title} [PLAYLIST]\n"
                await ctx.send(f"songs are in chronological order```\n{playlist}\n```")
            else:
                await player.queue.put_wait(tracks[0])

        if not player.playing:
            track = player.queue.get()
            try:
                await player.play(track)
            except wavelink.QueueEmpty:
                if has_choice:
                    await ctx.send("You didn't pick a search option!")
                else:
                    await ctx.send("queue is empty...")
            await ctx.guild.change_voice_state(channel=player.channel, self_mute=False, self_deaf=True)
        else:
            added_embed = discord.Embed()
            if isinstance(tracks, wavelink.Playlist):
                added_embed.description = f"Added {songs} to the queue"
            else:
                if has_choice:
                    added_embed.description = f"Added {choice_track.title} to the queue"
                else:
                    song = tracks[0]
                    added_embed.description = f"Added {song.title} to the queue"
                await ctx.send(embed=added_embed)

    @commands.command()
    async def disconnect(self, ctx: commands.Context):
        player = await check_and_send(ctx, default_response)
        if not player:
            return
        player.queue.clear()
        await player.disconnect()
        await ctx.message.add_reaction(self.config["emotes"]["success"])

    @commands.command(aliases=["loop"])
    async def repeat(self, ctx: commands.Context):
        player = await check_and_send(ctx, default_response)
        if not player:
            return

        async def send_stop_message():
            player.queue.mode = wavelink.QueueMode.normal
            await ctx.send("Stopped looping...")

        print(player.queue.mode)
        if player.queue.mode == wavelink.QueueMode.loop:
            await send_stop_message()
            return
        elif player.queue.mode == wavelink.QueueMode.loop_all:
            await send_stop_message()
            return
        try:
            def check(m):
                return m.author == ctx.author

            await ctx.send("Loop the queue or *track*?")

            collector = await self.bot.wait_for("message", check=check, timeout=25)

            if collector.content == "queue":
                player.queue.mode = wavelink.QueueMode.loop_all
                await ctx.send("Looping the queue.")
            elif collector.content == "track":
                player.queue.mode = wavelink.QueueMode.loop
                await ctx.send("Looping the track.")
            else:
                await ctx.send("Invalid option.")
        except asyncio.TimeoutError:
            await ctx.send("You didn't pick a option in time!")

    @commands.command(aliases=["mix"])
    async def shuffle(self, ctx: commands.Context):
        player = await check_and_send(ctx, default_response)
        if not player:
            return
        player.queue.shuffle()
        await ctx.send("Mixed up the queue...")

    @commands.command()
    async def pause(self, ctx: commands.Context):
        player = await check_and_send(ctx, default_response)
        if not player:
            return
        await ctx.send(f"Track {'paused' if not player.paused else 'un-paused'}")
        await ctx.send(
            f"to {'un-pause' if not player.paused else 'pause'}"
            f"run {get_config()['prefix']}pause again"
        )
        await player.pause(not player.paused)

    @commands.command()
    async def skip(self, ctx: commands.Context):
        player = await check_and_send(ctx, default_response)
        if not player:
            return
        await player.skip()
        await ctx.message.add_reaction(self.config["emotes"]["success"])

    @commands.command()
    async def volume(self, ctx: commands.Context, *, vol: int):
        player = await check_and_send(ctx, default_response)
        if not player:
            return
        await player.set_volume(vol)
        await ctx.message.add_reaction(self.config["emotes"]["success"])

    @commands.command()
    async def queue(self, ctx: commands.Context):
        player = await check_and_send(ctx, "Queue is not available")
        if not player:
            return

        output = ""
        que = list(player.queue)
        que.reverse()
        ln = 15 if len(que) > 15 else len(que)
        for i in range(ln):
            track = que[i]
            output += f"{i + 1}: {track.title}\n"

        if len(que) > 15:
            output += f"... {len(que) - ln} in queue ..."

        if (len(que)) == 0:
            output = "Queue is empty..."

        await ctx.send(f"```\n{output}\n```")


async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))

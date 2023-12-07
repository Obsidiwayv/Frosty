import os
from io import BytesIO
from math import isnan
from typing import cast
from PIL import ImageFont, Image, ImageDraw
from discord.ext import commands

import requests
import discord
import wavelink
import asyncio

from utils import get_config

voice_ids = {}
default_response = "I'm not in any voice channel!"


async def check_and_send(ctx: commands.Context, message: str):
    player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
    if not player:
        await ctx.send(message)
        return False
    return player


async def draw_song_interface(name, time, artist, thumbnail_size, cover: str):
    song_cover_image = Image.open(requests.get(cover, stream=True).raw)

    # Create a modern interface image
    width, height = 800, 200

    # Convert the song cover image to RGBA mode
    song_cover_image = song_cover_image.convert("RGBA")

    # Create a thumbnail of the song cover
    thumbnail_cover = song_cover_image.copy()
    thumbnail_cover.thumbnail(thumbnail_size)

    # Calculate the position to place the thumbnail on the side
    thumbnail_position = (20, (height - thumbnail_size[1]) // 2)

    # Create an empty RGBA image
    modern_interface_image = Image.new("RGBA", (width, height), (2, 4, 3))

    # Paste the song cover thumbnail on the side
    modern_interface_image.paste(thumbnail_cover, thumbnail_position, thumbnail_cover)

    # Draw additional elements (title, time, etc.) on the other side
    font_size = 30
    font = ImageFont.truetype(
        os.path.join(
            os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__), ".."
                )
            ),
            "FiraSans-Bold.ttf"
        ),
        font_size
    )

    font_anurati_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), "Anurati.otf")
    font_anurati = ImageFont.truetype(font_anurati_path, 30)

    total_seconds = time // 1000

    # Calculate hours, minutes, and seconds
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    draw = ImageDraw.Draw(modern_interface_image)
    draw.text((220, height - 120), f"{artist} - {name}", fill="white", font=font)
    draw.text((220, height - 70), f"time: {minutes}:{seconds}", fill="white", font=font)
    draw.text((340, height - 170), "Now playing:", fill="white", font=font_anurati)

    # Save the image to a temporary file
    image_path = "modern_interface.png"
    modern_interface_image.save(image_path)

    return image_path


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config = get_config()

    @commands.Cog.listener()
    async def on_wavelink_track_start(self, payload: wavelink.TrackStartEventPayload):
        ts = 180
        image_path = await draw_song_interface(
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
                    waited = await self.bot.wait_for("message", timeout=10, check=check)
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

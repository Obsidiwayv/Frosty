from typing import cast

from discord.ext import commands

import discord
import wavelink
import asyncio

from utils import get_config

voice_ids = {}
default_response = "I'm not in any voice channel!"

emoji_1 = "1️⃣"
emoji_2 = "2️⃣"
emoji_3 = "3️⃣"
emoji_4 = "4️⃣"
emoji_5 = "5️⃣"
emoji_6 = "6️⃣"
emoji_7 = "7️⃣"
emoji_8 = "8️⃣"


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
        started_embed = discord.Embed()
        started_embed.description = f"Now playing [{payload.track.title}]({payload.track.uri})"
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

                while s <= 7:
                    song_data = tracks[s]
                    songs_list += f"{s + 1}. {song_data.author} - {song_data.title}\n"
                    s += 1

                choice_message = await ctx.send(f"```\n{songs_list}\n```")
                await choice_message.add_reaction(emoji_1)
                await choice_message.add_reaction(emoji_2)
                await choice_message.add_reaction(emoji_3)
                await choice_message.add_reaction(emoji_4)
                await choice_message.add_reaction(emoji_5)
                await choice_message.add_reaction(emoji_6)
                await choice_message.add_reaction(emoji_7)
                await choice_message.add_reaction(emoji_8)

                await asyncio.sleep(10)

                got_choice_message = await ctx.channel.fetch_message(choice_message.id)

                # removing everyone else's reactions first
                for r in got_choice_message.reactions:
                    async for u in r.users():
                        if not u.id == ctx.author.id:
                            if not u.id == ctx.me.id:
                                await r.remove(u)

                for reaction in got_choice_message.reactions:
                    if reaction.emoji == emoji_1 and reaction.count == 2:
                        await player.queue.put_wait(tracks[0])
                        choice_track = tracks[0]
                        has_choice = True
                    elif reaction.emoji == emoji_2 and reaction.count == 2:
                        await player.queue.put_wait(tracks[1])
                        choice_track = tracks[1]
                        has_choice = True
                    elif reaction.emoji == emoji_3 and reaction.count == 2:
                        await player.queue.put_wait(tracks[2])
                        choice_track = tracks[2]
                        has_choice = True
                    elif reaction.emoji == emoji_4 and reaction.count == 2:
                        await player.queue.put_wait(tracks[3])
                        choice_track = tracks[3]
                        has_choice = True
                    elif reaction.emoji == emoji_5 and reaction.count == 2:
                        await player.queue.put_wait(tracks[4])
                        choice_track = tracks[4]
                        has_choice = True
                    elif reaction.emoji == emoji_6 and reaction.count == 2:
                        await player.queue.put_wait(tracks[5])
                        choice_track = tracks[5]
                        has_choice = True
                    elif reaction.emoji == emoji_7 and reaction.count == 2:
                        await player.queue.put_wait(tracks[6])
                        choice_track = tracks[6]
                        has_choice = True
                    elif reaction.emoji == emoji_8 and reaction.count == 2:
                        await player.queue.put_wait(tracks[7])
                        choice_track = tracks[7]
                        has_choice = True

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
        await player.pause(not player.paused)
        await ctx.message.add_reaction(self.config["emotes"]["success"])

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

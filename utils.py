import discord
import gd


def create_level_embed(level: gd.Level):
    embed = discord.Embed(title=f"{level.name} ({level.creator})", description=level.description)
    embed.add_field(name="coins", value=level.coins, inline=True)
    embed.add_field(name="Length", value=level.length, inline=True)
    embed.add_field(name="Difficulty", value=level.difficulty)
    return embed

import discord
import re

from utils import get_config


class MessageModule:
    def __init__(self, event: discord.Message):
        self.event = event
        self.config = get_config()

    async def init_gif(self):
        if isinstance(self.event.channel, discord.DMChannel):
            return
        regex = (
            fr'(?:view\/)?({re.escape("trollszn123-ronaldo-gif-18268194")}'
            fr'|{re.escape("boOys" + ".gif")})'
        )
        for snowflake in self.config["guilds"]:
            if self.event.guild.id == snowflake and bool(
                    re.search(re.escape("https://tenor.com/") + regex, self.event.content)):
                await self.event.delete()
            elif self.event.guild.id == snowflake and self.config["owner_id"] == self.event.author.id:
                if bool(re.match(
                        r"^https:\/\/tenor\.com\/(?:view\/)?[\w\d\u0080-\uFFFF%-]+(?:\.gif)?$",
                        self.event.content
                )):
                    if self.event.reference:
                        await self.event.channel.send(content=self.event.content, reference=self.event.reference)
                    else:
                        await self.event.channel.send(self.event.content)
                    await self.event.delete()

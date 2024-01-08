import discord

import dragon

class Colours:
    cyan = '\033[96m'
    green = '\033[92m'
    warning = '\033[93m'
    fail = '\033[91m'
    end = '\033[0m'


def log_format(txt: str, colour: str):
    return f"{colour}{txt}{Colours.end}"


def log_success(txt: str):
    print(log_format(txt, Colours.green))


def log_info(txt: str):
    print(log_format(txt, Colours.cyan))


def log_warn(txt: str):
    print(log_format(txt, Colours.warning))


def log_error(txt: str):
    print(log_format(txt, Colours.fail))


def log_user(message: discord.Message):
    print(log_info(
        f"[{message.author.id}][{message.author.name}]: [{message.channel.name}] >> {message.content}"
    ))
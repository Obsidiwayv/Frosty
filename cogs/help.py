# Code was copied from this repository: https://github.com/zedchance/embed_help

import discord
from discord.ext import commands

import utils

config = utils.get_config()
prefix = config['prefix']
bot_title = 'Octane help command'
bot_description = ''
bottom_info = ''


class Help(commands.Cog):
    """ Help commands """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='help',
                      description='Help command',
                      aliases=['info', 'commands'],
                      case_insensitive=True)
    async def help_command(self, ctx: commands.Context, *commands: str):
        """ Shows this message """
        bot = ctx.bot
        embed = discord.Embed(title=bot_title, description=bot_description)

        def generate_usage(command_name):
            """ Generates a string of how to use a command """
            temp = f'{prefix}'
            command = bot.get_command(command_name)
            # Aliases
            if len(command.aliases) == 0:
                temp += f'{command_name}'
            elif len(command.aliases) == 1:
                temp += f'[{command.name}|{command.aliases[0]}]'
            else:
                t = '|'.join(command.aliases)
                temp += f'[{command.name}|{t}]'
            # Parameters
            params = f' '
            for param in command.clean_params:
                params += f'<{command.clean_params[param]}> '
            temp += f'{params}'
            return temp

        def generate_command_list(cog):
            """ Generates the command list with properly spaced help messages """
            # Determine longest word
            max_length = 0
            for command in bot.get_cog(cog).get_commands():
                if not command.hidden:
                    if len(f'{command}') > max_length:
                        max_length = len(f'{command}')

            # Build list
            temp = ""
            for command in bot.get_cog(cog).walk_commands():
                if command.hidden:
                    temp += ''
                elif command.help is None:
                    if command.parent:
                        temp += f'{command.name}, '
                    else:
                        temp += f'{command}, '
                else:
                    temp += f'`{command}`'
                    for i in range(0, max_length - len(f'{command}') + 1):
                        temp += '   '
                    temp += f'{command.help}\n'
            return temp

        # Helper function to add fields to the embed
        async def add_field_to_embed(name, value, inline=True):
            field_count: int = 0
            embed.add_field(name=name, value=value, inline=inline)
            field_count += 1
            if field_count == 25:
                # If 25 fields reached, send the current embed and reset counters
                await ctx.send(embed=embed)
                embed.clear_fields()
                field_count = 0

        # Help by itself just lists our own commands.
        if len(commands) == 0:
            for cog in bot.cogs:
                temp = generate_command_list(cog)
                if temp != "":
                    await add_field_to_embed(name=f'**{cog}**', value=temp, inline=True)
            if bottom_info != "":
                await add_field_to_embed(name="Info", value=bottom_info, inline=True)
        elif len(commands) == 1:
            # Try to see if it is a cog name
            name = commands[0].capitalize()
            command = None

            if name in bot.cogs:
                cog = bot.get_cog(name)
                msg = generate_command_list(name)
                embed.add_field(name=name, value=msg, inline=False)
                msg = f'{cog.description}\n'
                embed.set_footer(text=msg)

            # Must be a command then
            else:
                command = bot.get_command(name)
                if command is not None:
                    help = f''
                    if command.help is not None:
                        help = command.help
                    embed.add_field(name=f'**{command}**',
                                    value=f'{command.description}```{generate_usage(name)}```\n{help}',
                                    inline=True)
                else:
                    msg = ' '.join(commands)
                    embed.add_field(name="Not found", value=f'Command/category `{msg}` not found.')
        else:
            msg = ' '.join(commands)
            embed.add_field(name="Not found", value=f'Command/category `{msg}` not found.')
            
        embed.colour = 0x00FF7F
        embed.set_image(url="https://wayvsite.space/octane_banner.png")

        await ctx.send(embed=embed)
        return


# Cog setup
async def setup(bot):
    await bot.add_cog(Help(bot))

import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound

import config
from config import COLOUR
from bottoken import TOKEN

from func import memdata, savememdata
import os
import traceback

TEST_MODE = True
DISABLE_EXT = ['testfuncs.py, ', '__pycache__', 'cog1.py']

intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix=config.PREFIX, intents=intents)


@client.event
async def on_ready():
    print('''
||                    BOT READY                    ||
-----------------------------------------------------''')
    print('GUILD ID             | GUILD NAME           | MEMBERS')
    for guild in client.guilds:
        print(f'{guild.id:<20} | {guild.name:<20} | {guild.member_count:>5,}')
    print()

    # load extensions
    loaded = []
    failed = []
    for filename in os.listdir('./cogs'):

        try:
            if not filename in DISABLE_EXT:
                await client.load_extension(f'cogs.{filename[:-3]}')
                loaded.append(filename)

        except Exception as e:
            print(e)
            print(f'**EXTENSION FAILED**: {filename}')
            failed.append(filename)
            # traceback.print_stack()

            traceback.print_tb(e.__traceback__)

    print(f'**Extensions Loaded: {loaded}')
    print(f'**Extensions Failed: {failed}')

    if TEST_MODE == True:
        return

    else:

        # online indicator for The K-Hole: #shit-fuck
        channel = client.get_channel(1159964516340224030)
        await channel.send("Beep boop, we're off the goop!")

        # online indicator for every guild
        for guild in client.guilds:
            try:
                channel = guild.system_channel
                await channel.send("Beep boop, we're off the goop!")

            except Exception as e:
                print(
                    f'''**Failed to send greeting in {guild.name} {channel}
                    {e}
                    ''')
                traceback.print_stack()

            # embed
            embed = discord.Embed(
                title='Beep Boop', color=COLOUR['System'])
            embed.add_field(name=':white_check_mark:Load Succes', value='\n'.join(
                f"{filename}" for filename in loaded), inline=True)
            embed.add_field(name=':no_entry:Load Failure', value='\n'.join(
                f"{filename}" for filename in failed), inline=True)


@client.command()
async def reload(ctx):
    loaded = []
    failed = []
    for filename in os.listdir('./cogs'):
        try:
            if not filename in DISABLE_EXT:
                await client.reload_extension(f'cogs.{filename[:-3]}')
                loaded.append(filename)

        except Exception as e:
            print(f'**FAILED**: {filename}')
            failed.append(filename)
            # traceback.print_stack()
            traceback.print_tb(e.__traceback__)
            print(e)

    print(f'**Extensions Reloaded: {loaded}')
    print(f'**Extensions Failed: {failed}')

    embed = discord.Embed(title='Extensions Reloaded',
                          color=COLOUR['System'])
    embed.add_field(name=':white_check_mark:Load Succes', value='\n'.join(
        f"{filename}" for filename in loaded), inline=True)
    embed.add_field(name=':no_entry:Load Failure', value='\n'.join(
        f"{filename}" for filename in failed), inline=True)

    await ctx.send(embed=embed)


@client.event
async def on_message(message):
    print(f'''{message.created_at} {message.author} ({message.author.id}) in {message.guild} #{message.channel}:
"{message.content}"
''')
    await client.process_commands(message)

    if str(message.author.id) not in memdata:
            # updates memdata
        memdata[str(message.author.id)] = {
            'name': str(message.author), 'crime_coeff': 0}
        print(f'added {message.author} ({message.author.id}) to memdata')
        savememdata()


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        embed = discord.Embed(color=config.COLOUR['Fail'])
        embed.add_field(
            name='', value=f'Command not found. Use ``{config.PREFIX}help`` to view available commands', inline=True)
        await ctx.send(embed=embed)


@client.event
async def on_member_join(member):
    # channel = client.get_channel(1155931099357253672)
    userid = member.id
    print(f'{member} ({userid}) joined {member.guild}')
    await member.send(f'{member} has joined the cosmic gnar gnar.')


@client.event
async def on_member_remove(member):
    channel = client.get_channel(1155931099357253672)
    await channel.send(f'{member} has returned to void.')

client.run(TOKEN)

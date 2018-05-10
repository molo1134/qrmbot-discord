#!/usr/bin/env python3

import discord
from discord.ext import commands
import asyncio
import json
import logging

logging.basicConfig(level=logging.INFO)

description = '''A bot for various ham radio functions.'''

bot = commands.Bot(command_prefix='?', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(game=discord.Game(name='with Lids on 7.200'))


@bot.command()
async def activity():
    """Band activity from PSKReporter"""
    await bot.say(result)
    # try:
    #     rolls, limit = map(int, dice.split('d'))
    # except Exception:
    #     await bot.say('Format has to be in NdN!')
    #     return

    # result = ''
    await bot.say(result)

@bot.command()
async def bands():
    """Display Propagation Information"""
    await bot.say(result)

@bot.command()
async def contests():
    """List current and upcoming contests"""
    await bot.say(result)

@bot.command()
async def dxcc(prefix : str):
    """Display information on a DXCC entity"""
    await bot.say(result)

@bot.command()
async def eqsl(callsign : str):
    """Last login to eQSL.cc for a callsign"""
    await bot.say(result)

@bot.command()
async def kf():
    """Display KP index predictions"""
    await bot.say(result)

@bot.command()
async def lotw(callsign : str):
    """Last upload date to LotW for a callsign"""
    await bot.say(result)

@bot.command()
async def call(callsign : str):
    """lookup a callsign on HamQTH?"""
    await bot.say(callsign)

@bot.command()
async def qth(*, query : str):
    """look up a grid square or QTH"""
    await bot.say(query)

# @bot.command()
# async def grid():
#     """alias for qth"""
#     await bot.say('test')

@bot.command()
async def spots(callsign : str):
    """display spots for a callsign"""
    await bot.say(result)

@bot.command()
async def units():
    """convert values between units, general purpose calculations"""
    await bot.say(result)

@bot.command()
async def utc():
    """display the current time in UTC"""
    await bot.say(result)

# @bot.command()
# async def z():
#     """alias for utc"""
#     await bot.say(result)

@bot.command()
async def wx(*, loc : str):
    """display current weather conditions"""
    await bot.say(result)

# @bot.command()
# async def wxfull():
#     """display more current weather conditions"""
#     await bot.say(result)

@bot.command()
async def morse(*, message : str):
    """convert to morse code"""
    await bot.say(result)

# @bot.command()
# async def cw():
#     """alias for morse"""
#     await bot.say(result)

@bot.command()
async def unmorse(*, message : str):
    """decode from morse"""
    await bot.say(result)

# @bot.command()
# async def demorse():
#     """alias for unmorse"""
#     await bot.say(result)

@bot.command()
async def kindex():
    """3 day k-index forecast"""
    await bot.say(result)

# @bot.command()
# async def ki():
#     """alias for kindex"""
#     await bot.say(result)

@bot.command()
async def forecast():
    """27 day solar forecast"""
    await bot.say(result)

@bot.command()
async def phoneticise(*, message : str):
    """random phonetics"""
    await bot.say(result)

# @bot.command()
# async def phoneticize():
#     """random phonetics"""
#     await bot.say(result)

# @bot.command()
# async def phonetics():
#     """random phonetics"""
#     await bot.say(result)

@bot.command()
async def repeater(callsign : str):
    """look up repeater by callsign"""
    await bot.say(result)

@bot.command()
async def muf(loc : str):
    """max useable frequency reports from ionosondes"""
    await bot.say(result)

# @bot.command()
# async def muf2():
#     """alt data sources for MUF"""
#     await bot.say(result)

@bot.command()
async def aprs(callsign : str):
    """APRS station info"""
    await bot.say(result)

@bot.command()
async def sun(loc : str):
    """sun position"""
    await bot.say(result)

@bot.command()
async def moon(loc : str):
    """moon position"""
    await bot.say(result)

@bot.command()
async def eme():
    """EME 2m propagation information"""
    await bot.say(result)

@bot.command()
async def graves():
    """GRAVES radar EME beacon status"""
    await bot.say(result)

@bot.command()
async def sat(bird : str, loc : str):
    """satellite pass predictor"""
    await bot.say(result)

@bot.command()
async def qcode(query : str):
    """Q code lookup"""
    await bot.say(result)

# @bot.command()
# async def q():
#     """alias of qcode"""
#     await bot.say(result)

#########################

with open('secrets.json') as secrets_file:
    secrets = json.load(secrets_file)

bot.run(secrets['token'])


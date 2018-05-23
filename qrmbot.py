#!/usr/bin/env python3

import discord
from discord.ext import commands
import asyncio
import json
import logging
import random
import datetime

logging.basicConfig(level=logging.INFO)

description = '''QRM'''
pfx = '?'

bot = commands.Bot(command_prefix=pfx, description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(game=discord.Game(name='with Lids on 7.200'))

@bot.command(aliases=['x'])
async def xkcd(num : str):
    """Gets an xkcd by number (Alias: x)"""
    await bot.say("http://xkcd.com/" + num)

@bot.command(aliases=['q'])
async def qcode(q : str):
    """Look up a Q Code (Alias: q)"""
    q = q.upper()
    try:
        code = qcodes[q]
        await bot.say(q + ' = ' + code)
    except:
        await bot.say(q + ' not found.')

@bot.command(aliases=['phoneticize', 'phoneticise', 'phone'])
async def phonetics(*, msg : str):
    """Get phonetics for a word or phrase (Alias: phoneticize, phoneticise, phone)"""
    result = ''
    for char in msg:
        if char.isalpha():
            w = [word for word in WORDS if (word[0] == char)]
            result += w[random.randint(0,len(w)-1)]
        else:
            result += char
        result += ' '
    await bot.say(result.title())

@bot.command(aliases=['cw'])
async def morse(*, msg : str):
    '''Converts ASCII to international morse code (Alias: cw)'''
    result = ''
    for char in msg.upper():
        try:
            result += ascii2morse[char]
        except:
            result += '<?>'
        result += ' '
    await bot.say(result)

@bot.command(aliases=['demorse'])
async def unmorse(*, msg : str):
    '''Converts international morse code to ASCII (Alias: demorse)'''
    result = ''
    msg = msg.split('/')
    msg = [m.split() for m in msg]
    for word in msg:
        for char in word:
            try:
                result += morse2ascii[char]
            except:
                result += '<?>'
        result += ' '
    await bot.say(result)

@bot.command(aliases=['z'])
async def utc():
    '''Gets the current time in UTC (Alias: z)'''
    d = datetime.datetime.utcnow()
    result = d.strftime('%Y-%m-%d %H:%M') + 'Z'
    await bot.say(result)


#########################

WORDS = open('words').read().splitlines()

with open('morse.json') as morse_file:
    ascii2morse = json.load(morse_file)
    morse2ascii = {v:k for k,v in ascii2morse.items()}

with open('qcodes.json') as qcode_file:
    qcodes = json.load(qcode_file)

with open('secrets.json') as secrets_file:
    secrets = json.load(secrets_file)

bot.run(secrets['token'])


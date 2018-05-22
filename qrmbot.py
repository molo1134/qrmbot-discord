#!/usr/bin/env python3

import discord
from discord.ext import commands
import asyncio
import json
import logging
import random

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

#########################

WORDS = open('words').read().splitlines()

with open('qcodes.json') as qcode_file:
    qcodes = json.load(qcode_file)

with open('secrets.json') as secrets_file:
    secrets = json.load(secrets_file)

bot.run(secrets['token'])


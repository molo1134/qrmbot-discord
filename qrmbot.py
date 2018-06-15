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
lastq = {}

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
            result += random.choice(w)
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

@bot.command(aliases=['ae'])
async def ae7q(call : str):
    '''Links to info about a callsign from AE7Q. Alias: ae'''
    await bot.say(f'http://ae7q.com/query/data/CallHistory.php?CALL={call}')

@bot.command(aliases=['dx'])
async def dxcc(q : str):
    '''Gets info about a prefix. Alias: dx'''
    q = q.upper()
    if q in CTY_list:
        d = CTY[q]
        prefix = q
        entity = d['entity']
        cqzone = d['cq']
        ituzone = d['itu']
        continent = d['continent']
        tz = d['tz']
        if tz > 0:
            tz = '+' + str(tz)

        res = f'''**{prefix}:** {entity}
    *CQ Zone:* {cqzone}
    *ITU Zone:* {ituzone}
    *Continent:* {continent}
    *Time Zone:* UTC{tz}'''
    else:
        res = f'Prefix {q} not found'
    await bot.say(res)

@bot.command(pass_context=True)
async def plan(ctx):
    '''Posts an image of the US Frequency Allocations'''
    await bot.send_file(ctx.message.channel, 'band-chart.png')

@bot.command(aliases=['randomq'], pass_context=True)
async def rq(ctx, level: str = None):
    '''Gets a random question from the Technician/General/Extra question pools'''

    # we'll set the pool now, so if the user didn't provide one we don't have to make a special case for that later
    selected_pool = random.choice([tech_pool, gen_pool, extra_pool])
    level = level.lower()

    if level == "t":
        selected_pool = tech_pool
    if level == "technician":
        selected_pool = tech_pool
    if level == "tech":
        selected_pool = tech_pool

    if level == "gen":
        selected_pool = gen_pool
    if level == "g":
        selected_pool = gen_pool
    if level == "general":
        selected_pool = gen_pool

    if level == "e":
        selected_pool = extra_pool
    if level == "extra":
        selected_pool = extra_pool

    question = random.choice(selected_pool)
    embed = discord.Embed(title=question['number'], colour=0x2dc614)
    embed = embed.add_field(name="Question:", value=question["text"], inline=False)
    embed = embed.add_field(name="Answers:", value=
                            "**A:** " + question["answers"][0] +
                            "\n**B:** " + question["answers"][1] +
                            "\n**C:** " + question["answers"][2] +
                            "\n**D:** " + question["answers"][3], inline=False)
    embed = embed.add_field(name="Answer:", value="Type _?rqa_ for answer", inline=False)
    global lastq
    lastq[ctx.message.channel.id] = question["answer"]
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def rqa(ctx):
    '''Returns the answer to question asked.'''
    global lastq
    await bot.say(lastq[ctx.message.channel.id])

#########################

WORDS = open('words').read().splitlines()

with open('cty.json') as ctyfile:
    CTY = json.load(ctyfile)
    CTY_list = list(CTY.keys())
    CTY_list.sort()
    CTY_list.sort(key=len, reverse=True)

with open('morse.json') as morse_file:
    ascii2morse = json.load(morse_file)
    morse2ascii = {v: k for k, v in ascii2morse.items()}

with open('qcodes.json') as qcode_file:
    qcodes = json.load(qcode_file)

with open('secrets.json') as secrets_file:
    secrets = json.load(secrets_file)

with open("Tech.json") as f:
    tech_pool = json.load(f)

with open("General.json") as f:
    gen_pool = json.load(f)

with open("Extra.json") as f:
    extra_pool = json.load(f)

bot.run(secrets['token'])


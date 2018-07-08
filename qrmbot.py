#!/usr/bin/env python3

import discord
from discord.ext import commands
import asyncio
import json
import logging
import random
from datetime import datetime

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
    d = datetime.utcnow()
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
    if q != 'last_updated':
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

    selected_pool = None
    try:
        level = level.lower()
    except AttributeError:  # no level given (it's None)
        pass

    if level in ["t", "technician", "tech"]:
        selected_pool = tech_pool

    if level in ["g", "gen", "general"]:
        selected_pool = gen_pool

    if level in ["e", "extra"]:
        selected_pool = extra_pool

    if (level is None) or (level == "all"):  # no pool given or user wants all, so pick a random pool and use that
        selected_pool = random.choice([tech_pool, gen_pool, extra_pool])
    if (level is not None) and (selected_pool is None):  # unrecognized pool given by user
        await bot.say("The question pool you gave was unrecognized. " +
                      "There are many ways to call up certain question pools- try ?rq t, g, or e. " +
                      "(Note that only the US question pools are available.)")
        return

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
    lastq[ctx.message.channel.id] = (question['number'], question["answer"])
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def rqa(ctx, ans : str = None):
    '''(Optional argument: your answer) Returns the answer to question asked.'''
    global lastq
    correct_ans = lastq[ctx.message.channel.id][1]
    q_num = lastq[ctx.message.channel.id][0]
    if ans is not None:
        ans = ans.upper()
        if ans == correct_ans:
            result = f"Correct! The answer to {q_num} was **{correct_ans}**."
        else:
            result = f"Incorrect. The answer to {q_num} was **{correct_ans}**, not **{ans}**."
    else:
        result = f"The correct answer to {q_num} was **{correct_ans}**."
    await bot.say(result)

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


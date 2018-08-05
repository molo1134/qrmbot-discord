#!/usr/bin/env python3

import discord
from discord.ext import commands
import asyncio
import json
import logging
import time
import random
from datetime import datetime
from cty_json import genCtyJson

logging.basicConfig(level=logging.INFO)

description = '''A bot with various useful ham radio-related functions.'''
pfx = '?'
lastq = {}

green = 0x2dc614
red = 0xc91628
blue = 0x2044f7

bot = commands.Bot(command_prefix=pfx, description=description)
bot.remove_command('help')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(game=discord.Game(name='with Lids on 7.200'))

@bot.event
async def on_message(message):
    try:
        content = message.content.split()
        content[0] = content[0].lower()
        message.content = ' '.join(content)
    except:
        pass
    await bot.process_commands(message)

@bot.command(aliases=['h'])
async def help(c : str = None):
    '''Show this message.'''
    embed = discord.Embed(title='Commands', description=bot.description, colour=green)
    cmds = sorted(list(set(bot.commands.values())), key=lambda x:x.name)
    for cmd in cmds:
        v = cmd.help
        if len(cmd.aliases) > 0:
            v += '\n*Aliases:* ?' +\
                f', {pfx}'.join(cmd.aliases).rstrip(f', {pfx}')
        embed = embed.add_field(name=pfx+cmd.name, value=v, inline=False)
    await bot.say(embed=embed)

@bot.command(aliases=['x'])
async def xkcd(num : str):
    '''Look up an xkcd by number.'''
    await bot.say('http://xkcd.com/' + num)

@bot.command(aliases=['q'])
async def qcode(q : str):
    '''Look up a Q Code.'''
    q = q.upper()
    try:
        code = qcodes[q]
        embed = discord.Embed(title=q, description=qcodes[q], colour=green)
    except:
        embed = discord.Embed(title=q, description='Q Code not found', colour=red)
    await bot.say(embed=embed)

@bot.command(aliases=['ph', 'phoneticize', 'phoneticise', 'phone'])
async def phonetics(*, msg : str):
    '''Get phonetics for a word or phrase.'''
    result = ''
    for char in msg:
        if char.isalpha():
            w = [word for word in WORDS if (word[0] == char)]
            result += random.choice(w)
        else:
            result += char
        result += ' '
    embed = discord.Embed(title=f'Phonetics for {msg}', description=result.title(), colour=green)
    await bot.say(embed=embed)

@bot.command(aliases=['cw'])
async def morse(*, msg : str):
    '''Converts ASCII to international morse code.'''
    result = ''
    for char in msg.upper():
        try:
            result += ascii2morse[char]
        except:
            result += '<?>'
        result += ' '
    embed = discord.Embed(title=f'Morse Code for {msg}', description=result, colour=green)
    await bot.say(embed=embed)

@bot.command(aliases=['demorse'])
async def unmorse(*, msg : str):
    '''Converts international morse code to ASCII.'''
    result = ''
    msg0 = msg
    msg = msg.split('/')
    msg = [m.split() for m in msg]
    for word in msg:
        for char in word:
            try:
                result += morse2ascii[char]
            except:
                result += '<?>'
        result += ' '
    embed = discord.Embed(title=f'ASCII for {msg0}', description=result, colour=green)
    await bot.say(embed=embed)

@bot.command(aliases=['cww'])
async def weight(msg : str):
    '''Calculates the CW Weight of a callsign.'''
    msg = msg.upper()
    weight = 0
    for char in msg:
        try:
            cwChar = ascii2morse[char].replace('-', '==')
            weight += len(cwChar) * 2 + 2
        except:
            res = f'Unknown character {char} in callsign'
            await bot.say(res)
            return
    res = f'The CW weight is **{weight}**'
    embed = discord.Embed(title=f'CW Weight of {msg}', description=res, colour=green)
    await bot.say(embed=embed)

@bot.command(aliases=['z'])
async def utc():
    '''Gets the current time in UTC.'''
    d = datetime.utcnow()
    result = '**' + d.strftime('%Y-%m-%d %H:%M') + 'Z**'
    embed = discord.Embed(title='The current time is:', description=result, colour=green)
    await bot.say(embed=embed)

@bot.command(aliases=['ae'])
async def ae7q(call : str):
    '''Links to info about a callsign from AE7Q.'''
    await bot.say(f'http://ae7q.com/query/data/CallHistory.php?CALL={call}')

@bot.command()
async def qrz(call : str):
    '''Links to info about a callsign from QRZ.'''
    await bot.say(f'http://qrz.com/db/{call}')
    
@bot.command(aliases=['dx'])
async def dxcc(q : str):
    '''Gets info about a prefix.'''
    noMatch = True
    qMatch = None
    q = q.upper()
    q0 = q
    if q != 'LAST_UPDATED':
        while noMatch:
            if q in CTY_list:
                qMatch = q
                noMatch = False
            else:
                q = q[:-1]
                if len(q) == 0:
                    noMatch = False
            if qMatch is not None:
                d = CTY[qMatch]
                prefix = qMatch
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
                clr = green
            else:
                res = f'Prefix {q0} not found'
                clr = red
        embed = discord.Embed(title=f'DXCC Info for {q0}', description=res, colour=clr)
    else:
        updatedDate =  CTY['last_updated'][0:4] + '-'
        updatedDate += CTY['last_updated'][4:6] + '-'
        updatedDate += CTY['last_updated'][6:8]
        res = f'CTY.DAT last updated on {updatedDate}'
        embed = discord.Embed(title=res, colour=blue)
    await bot.say(embed=embed)

@bot.command(aliases=['bands'])
async def plan(msg : str = ''):
    '''Posts an image of Frequency Allocations.
    Optional argument: `cn` = China, `ca` = Canada, `us` = USA.'''
    if msg.lower() == 'cn':
        embed = discord.Embed(title='Chinese Amateur Radio Bands',
            colour=green)
        embed.set_image(url='https://cdn.discordapp.com/attachments/364489754839875586/468770333223157791/Chinese_Amateur_Radio_Bands.png')
    elif msg.lower() == 'ca':
        embed = discord.Embed(title='Canadian Amateur Radio Bands',
            colour=green)
        embed.set_image(url='https://cdn.discordapp.com/attachments/448839119934717953/469972377778782208/RAC_Bandplan_December_1_2015-1.png')
    else:
        embed = discord.Embed(title='US Amateur Radio Bands',
            colour=green)
        embed.set_image(url='https://cdn.discordapp.com/attachments/377206780700393473/466729318945652737/band-chart.png')
    await bot.say(embed=embed)

@bot.command()
async def map(msg : str = ''):
    '''Posts an image of Frequency Allocations.
    Optional argument:`cq` = CQ Zones, `itu` = ITU Zones, `arrl` or `rac` =
    ARRL/RAC sections, `us` = US Callsign Areas.'''
    if msg.lower() == 'cq':
        embed = discord.Embed(title='Worldwide CQ Zones Map',
            colour=green)
        embed.set_image(url='https://cdn.discordapp.com/attachments/427925486908473344/472856720142761985/cq-zone.png')
    elif msg.lower() == 'itu':
        embed = discord.Embed(title='Worldwide ITU Zones Map',
            colour=green)
        embed.set_image(url='https://cdn.discordapp.com/attachments/427925486908473344/472856796235563018/itu-zone.png')
    elif msg.lower() == 'arrl' or msg.lower() == 'rac':
        embed = discord.Embed(title='ARRL/RAC Section Map',
            colour=green)
        embed.set_image(url='https://cdn.discordapp.com/attachments/427925486908473344/472856898220064778/sections.png')
    else:
        embed = discord.Embed(title='US Callsign Areas',
            colour=green)
        embed.set_image(url='https://cdn.discordapp.com/attachments/427925486908473344/472856506476265497/WASmap_Color.png')
    await bot.say(embed=embed)

@bot.command(aliases=['randomq'], pass_context=True)
async def rq(ctx, level: str = None):
    '''Gets a random question from the Technician, General, and/or Extra question pools.'''

    selected_pool = None
    try:
        level = level.lower()
    except AttributeError:  # no level given (it's None)
        pass

    if level in ['t', 'technician', 'tech']:
        selected_pool = tech_pool

    if level in ['g', 'gen', 'general']:
        selected_pool = gen_pool

    if level in ['e', 'extra']:
        selected_pool = extra_pool

    if (level is None) or (level == 'all'):  # no pool given or user wants all, so pick a random pool and use that
        selected_pool = random.choice([tech_pool, gen_pool, extra_pool])
    if (level is not None) and (selected_pool is None):  # unrecognized pool given by user
        await bot.say('The question pool you gave was unrecognized. ' +
                      'There are many ways to call up certain question pools - try ?rq t, g, or e. ' +
                      '(Note that only the US question pools are available).')
        return

    question = random.choice(selected_pool)
    embed = discord.Embed(title=question['number'], colour=green)
    embed = embed.add_field(name='Question:', value=question['text'], inline=False)
    embed = embed.add_field(name='Answers:', value=
                            '**A:** ' + question['answers'][0] +
                            '\n**B:** ' + question['answers'][1] +
                            '\n**C:** ' + question['answers'][2] +
                            '\n**D:** ' + question['answers'][3], inline=False)
    embed = embed.add_field(name='Answer:', value='Type _?rqa_ for answer', inline=False)
    global lastq
    lastq[ctx.message.channel.id] = (question['number'], question['answer'])
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def rqa(ctx, ans : str = None):
    '''Returns the answer to question last asked (Optional argument: your answer).'''
    global lastq
    correct_ans = lastq[ctx.message.channel.id][1]
    q_num = lastq[ctx.message.channel.id][0]
    if ans is not None:
        ans = ans.upper()
        if ans == correct_ans:
            result = f'Correct! The answer to {q_num} was **{correct_ans}**.'
            embed = discord.Embed(title=f'{q_num} Answer', description=result, colour=green)
        else:
            result = f'Incorrect. The answer to {q_num} was **{correct_ans}**, not **{ans}**.'
            embed = discord.Embed(title=f'{q_num} Answer', description=result, colour=red)
    else:
        result = f'The correct answer to {q_num} was **{correct_ans}**.'
        embed = discord.Embed(title=f'{q_num} Answer', description=result, colour=blue)
    await bot.say(embed=embed)

@bot.command()
async def grid(lat : str, lon : str):
    '''Calculates the grid square for latitude and longitude coordinates.
Usage: `?grid <lat> <lon>`
`lat` and `lon` are decimal coordinates, with negative being latitude South and longitude West.'''
    grid = "**"
    try:
        latf = float(lat) + 90
        lonf = float(lon) + 180
        if 0 <= latf <= 180 and 0 <= lonf <= 360:
            grid += chr(ord('A') + int(lonf / 20))
            grid += chr(ord('A') + int(latf / 10))
            grid += chr(ord('0') + int((lonf % 20)/2))
            grid += chr(ord('0') + int((latf % 10)/1))
            grid += chr(ord('a') + int((lonf - (int(lonf/2)*2)) / (5/60)))
            grid += chr(ord('a') + int((latf - (int(latf/1)*1)) / (2.5/60)))
            grid += "**"
            embed = discord.Embed(title=f'Maidenhead Grid Locator for {float(lat):.6f}, {float(lon):.6f}',
                    description=grid, colour=green)
        else:
            raise ValueError('Out of range.')
    except Exception as e:
        msg = f'Error generating grid square for {lat}, {lon}.'
        embed = discord.Embed(title=msg, description=str(e), colour=red)
    await bot.say(embed=embed)

@bot.command(aliases=['ungrid'])
async def loc(grid : str):
    try:
        grid = grid.upper()

        if len(grid) < 3:
            raise ValueError('The grid locator must be at least 4 characters long.')

        if not grid[0:2].isalpha() or not grid[2:4].isdigit():
            if len(grid) <= 4:
                raise ValueError('The grid locator must be of the form AA##.')
            elif len(grid) >= 6 and not grid[5:7].isalpha():
                raise ValueError('The grid locator must be of the form AA##AA.')

        lon = ((ord(grid[0]) - ord('A')) * 20) - 180;
        lat = ((ord(grid[1]) - ord('A')) * 10) - 90;
        lon += ((ord(grid[2]) - ord('0')) * 2);
        lat += ((ord(grid[3]) - ord('0')) * 1);

        if len(grid) >= 6:
            # have subsquares
            lon += ((ord(grid[4])) - ord('A')) * (5/60);
            lat += ((ord(grid[5])) - ord('A')) * (2.5/60);
            # move to center of subsquare
            lon += (2.5/60);
            lat += (1.25/60);
            # not too precise
            embed = discord.Embed(title=f'Latitude and Longitude for {grid}',
                    description=f'**{lat:.5f}, {lon:.5f}**', colour=green,
                    url=f'https://www.google.com/maps/place/{lat:.5f},{lon:.5f}/@{lat:.5f},{lon:.5f},13z')
        else:
            # move to center of square
            lon += 1;
            lat += 0.5;
            # even less precise
            embed = discord.Embed(title=f'Latitude and Longitude for {grid}',
                    description=f'**{lat:.1f}, {lon:.1f}**', colour=green,
                    url=f'https://www.google.com/maps/place/{lat:.1f},{lon:.1f}/@{lat:.1f},{lon:.1f},10z')
    except Exception as e:
        msg = f'Error generating latitude and longitude for grid {grid}.'
        embed = discord.Embed(title=msg, description=str(e), colour=red)

    await bot.say(embed=embed)


#########################

WORDS = open('words').read().splitlines()

@asyncio.coroutine
def updateCty():
    global CTY
    global CTY_list
    while True:
        print('Checking for CTY update...')
        try:
            firstRun
        except NameError:
            firstRun = True
        regen = genCtyJson()
        if regen or firstRun:
            with open('cty.json') as ctyfile:
                print('Reloading CTY JSON data...')
                CTY = json.load(ctyfile)
                CTY_list = list(CTY.keys())
                CTY_list.sort()
                CTY_list.sort(key=len, reverse=True)
            firstRun = False
        yield from asyncio.sleep(60*60*24)

ctyTask = asyncio.Task(updateCty())

with open('morse.json') as morse_file:
    ascii2morse = json.load(morse_file)
    morse2ascii = {v: k for k, v in ascii2morse.items()}

with open('qcodes.json') as qcode_file:
    qcodes = json.load(qcode_file)

with open('secrets.json') as secrets_file:
    secrets = json.load(secrets_file)

with open('Tech.json') as f:
    tech_pool = json.load(f)

with open('General.json') as f:
    gen_pool = json.load(f)

with open('Extra.json') as f:
    extra_pool = json.load(f)

bot.run(secrets['token'])


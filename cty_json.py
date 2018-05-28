#!/usr/bin/env python3
"""
Generates JSON from a CTY.DAT file

Format:
entity name: CQ Zone: ITU Zone: Continent: Latitude: Longitude: Time Zone: Primary Prefix:
    other,prefixes,and,=callsigns;
"""
import re
import json

with open('cty.dat') as ctyfile:
    cty = dict()
    last = ''
    while True:
        line = ctyfile.readline().rstrip('\x0D').strip(':')
        if not line:
            break
        if line != '' and line[0].isalpha():
            line = [x.strip() for x in line.split(':')]
            if line[7][0] == '*':
                line[7] = line[7][1:]
                line[0] += ' (not DXCC)'
            cty[line[7]] = {'entity':line[0], 'cq': int(line[1]),
                            'itu':int(line[2]), 'continent': line[3],
                            'lat':float(line[4]), 'long':float(line[5]),
                            'tz':-1*float(line[6]), 'len': len(line[7])}
            last = line[7]

        elif line != '' and line[0].isspace():
            line = line.strip().rstrip(';').rstrip(',').split(',')
            for i in line:
                if i not in cty.keys():
                    data = cty[last]
                    if re.search(r'\[(\d+)\]', i):
                        data['itu'] = int(re.search(r'\[(\d+)\]', i).group(1))
                    if re.search(r'\((\d+)\)', i):
                        data['cq'] = int(re.search(r'\((\d+)\)', i).group(1))
                    if re.search(r'<(\d+)\/(\d+)>', i):
                        data['lat'] = float(re.search(r'<(\d+)/(\d+)>', i).group(2))
                        data['long'] = float(re.search(r'<(\d+)/(\d+)>', i).group(2))
                    if re.search(r'\{(\w+)\}', i):
                        data['continent'] = re.search(r'\{(\w+)\}', i).group(1)
                    if re.search(r'~(\w+)~', i):
                        data['tz'] = -1 * float(re.search(r'\{(\w+)\}', i).group(1))
                    prefix = re.sub(r'=?([^\(\[]*)(\(\d+\))?(\[\d+\])?(<\d+\/\d+>)?(\{\w+\})?(~\w+~)?', r'\1', i)
                    cty[prefix] = data
with open('cty.json', 'w') as cty_json:
    json.dump(cty, cty_json)


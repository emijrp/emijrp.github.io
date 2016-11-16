#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2016 emijrp <emijrp@gmail.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import fileinput
import json

def main():
    preferedLangs = ['es', 'en', 'ca', 'gl', 'pt', 'it', 'fr', 'de', 
                     'eu', 'cz', 'hu', 'nl', 'sv', 'no', 'fi', 'ro', 
                     'eo', 'da','sk', 'tr']
    items = []
    c = 1
    for line in fileinput.input():
        line = line.strip().rstrip(',')
        if not line.startswith('{'):
            continue
        item = json.loads(line)
        if item['type'] != 'item':
            continue
        if not 'id' in item:
            continue
        
        language = ''
        label = ''
        if 'labels' in item:
            for prefLang in preferedLangs:
                if prefLang in item['labels']:
                    language = prefLang
                    label = item['labels'][prefLang]['value']
                    break
            if not label:
                availableLangs = list(item['labels'].keys())
                if availableLangs:
                    language = availableLangs[0]
                    label = item['labels'][language]['value']
        items.append([int(item['id'].split('Q')[1]), {'id': item['id'], 'language': language, 'label': label}])
        c += 1
        if c % 1000 == 0:
            print('Loaded', c, 'labels')
        if len(items) > 500000:
            break
    items.sort()
    #print('\n'.join(['%s, %s, %s' % (q, props['language'], props['label']) for id, q, props in items[:100]]))
    step = 100000
    output = {}
    c = 1
    for q, item in items:
        if q / step > c:
            with open('labels-q%d.json' % ((c-1)*step), 'w') as outfile:
                json.dump(output, outfile, sort_keys=True, indent=1, separators=(',', ': '))
            c += 1
            output = {}
        output[item['id']] = {'language': item['language'], 'label': item['label']}

if __name__ == '__main__':
    main()

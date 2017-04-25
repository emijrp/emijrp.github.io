#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2017 emijrp <emijrp@gmail.com>
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

import csv
import datetime
import json
import re
import sys
import urllib

def main():
    #Commons
    cat = 'Category:Files_by_User:Emijrp'
    api = 'https://commons.wikimedia.org/w/api.php'
    apiquery = '%s?action=query&generator=categorymembers&gcmtitle=%s&format=json' % (api, cat)
    uccontinue = True
    uccontinue_name = 'gcmcontinue'
    c = 0
    rows = []
    while uccontinue:
        sys.stderr.write(".")
        if uccontinue == True:
            json_data = urllib.urlopen(apiquery)
        else:
            json_data = urllib.urlopen(apiquery+'&'+uccontinue_name+'='+uccontinue)
        data = json.load(json_data)
        for pageid in data['query']['pages']:
            pagens = data['query']['pages'][pageid]['ns']
            pagetitle = data['query']['pages'][pageid]['title']
            if pagens != 6:
                continue
            
            #print(pageid, pagens, pagetitle)
            pagetitle_ = pagetitle.replace(' ', '_')
            apiquery2 = '%s?action=query&titles=%s&prop=imageinfo&iiprop=metadata&format=json' % (api, urllib.quote(pagetitle_.encode('utf-8')))
            json_data2 = urllib.urlopen(apiquery2)
            data2 = json.load(json_data2)
            originaldate = ''
            model = ''
            if data2['query']['pages'][pageid]['imageinfo'][0]['metadata']:
                for metadict in data2['query']['pages'][pageid]['imageinfo'][0]['metadata']:
                    if metadict['name'].lower() == 'datetimeoriginal':
                        originaldate = metadict['value'].strip()
                    if metadict['name'].lower() == 'model':
                        model = metadict['value'].strip()
            
            row = ['commons', pageid, pagetitle.encode('utf-8'), model, originaldate]
            rows.append(row)
            c += 1
        json_data.close()

        if data.has_key('continue'):
            uccontinue = data['continue'][uccontinue_name]
        else:
            uccontinue = ''
    print '\n', c, 'files in Commons'
    
    #Flickr
    
    #todo
    
    #Save CSV
    rows.sort()
    with open('photos.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in rows:
            writer.writerow(row)

if __name__ == '__main__':
    main()

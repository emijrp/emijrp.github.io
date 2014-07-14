#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Copyright (C) 2014 emijrp
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

import datetime
import json
import re
import sys
import urllib

def main():
    projects = [
        ['Emijrp', '15mpedia', 'http://wiki.15m.cc/w/api.php'], 
        ['Emijrp', 'Wikiindex', 'http://wikiindex.org/api.php'], 
        ['Emijrp', 'WikiPapers', 'http://wikipapers.referata.com/w/api.php'], 
        ['Emijrp', 'Wikipedia (en)', 'http://en.wikipedia.org/w/api.php'], 
        ['Emijrp', 'Wikipedia (es)', 'http://es.wikipedia.org/w/api.php'], 
    ]
    activity = {}
    total = 0
    for nick, project, api in projects:
        print '\n', nick, '@', project
        apiquery = '?action=query&list=usercontribs&ucuser=%s&uclimit=500&ucprop=timestamp|title|comment&format=json' % (nick)
        uccontinue = True
        uccontinue_name = 'uccontinue'
        subtotal = 0
        while uccontinue:
            sys.stderr.write(".")
            if uccontinue == True:
                json_data = urllib.urlopen(api+apiquery)
            else:
                json_data = urllib.urlopen(api+apiquery+'&'+uccontinue_name+'='+uccontinue)
            data = json.load(json_data)
            #print data
            for edit in data['query']['usercontribs']:
                #d = datetime.datetime.strptime(edit['timestamp'], "%Y-%m-%dT%H:%M:%SZ")
                d = datetime.datetime.strptime(edit['timestamp'].split('T')[0], "%Y-%m-%d")
                unixtime = d.strftime('%s')
                if activity.has_key(unixtime):
                    activity[unixtime] += 1
                else:
                    activity[unixtime] = 1
                subtotal += 1
                total += 1
            json_data.close()
            #print data
            if data.has_key('query-continue'):
                if not data['query-continue']['usercontribs'].has_key(uccontinue_name):
                    uccontinue_name = 'ucstart'
                uccontinue = data['query-continue']['usercontribs'][uccontinue_name]
            else:
                uccontinue = ''
            
            #print uccontinue
            #break
        print '\n', project, subtotal, 'ediciones'
    
    print '\nTotal', total, 'ediciones'
    
    with open('actividad.json', 'w') as outfile:
        outfile.write(json.dumps(activity, indent=4, sort_keys=True))

if __name__ == '__main__':
    main()

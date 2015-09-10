#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2014-2015 emijrp <emijrp@gmail.com>
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
        ['Emijrp', 'Cadizpedia', 'http://cadizpedia.wikanda.es/w/api.php'], 
        ['Emijrp', 'Commons', 'https://commons.wikimedia.org/w/api.php'], 
        ['Emijrp', 'Enciclopedia Libre', 'http://enciclopedia.us.es/api.php'], 
        ['Emijrp', 'Incubator', 'https://incubator.wikimedia.org/w/api.php'], 
        ['Emijrp', 'MediaWiki', 'https://www.mediawiki.org/w/api.php'], 
        ['Emijrp', 'Meta-Wiki', 'https://meta.wikimedia.org/w/api.php'], 
        ['Emijrp', 'No les votes', 'http://wiki.nolesvotes.org/w/api.php'], 
        ['Emijrp', 'WikiApiary', 'https://wikiapiary.com/w/api.php'], 
        ['Emijrp', 'Wikibooks (en)', 'https://en.wikibooks.org/w/api.php'], 
        ['Emijrp', 'Wikibooks (es)', 'https://es.wikibooks.org/w/api.php'], 
        ['Emijrp', 'Wikidata', 'https://www.wikidata.org/w/api.php'], 
        ['Emijrp', 'Wikiindex', 'http://wikiindex.org/api.php'], 
        ['Emijrp', 'Wikinews (en)', 'https://en.wikinews.org/w/api.php'], 
        ['Emijrp', 'Wikinews (es)', 'https://es.wikinews.org/w/api.php'], 
        ['Emijrp', 'WikiPapers', 'http://wikipapers.referata.com/w/api.php'], 
        ['Emijrp', 'Wikipedia (ca)', 'https://ca.wikipedia.org/w/api.php'], 
        ['Emijrp', 'Wikipedia (da)', 'https://da.wikipedia.org/w/api.php'], 
        ['Emijrp', 'Wikipedia (de)', 'https://de.wikipedia.org/w/api.php'], 
        ['Emijrp', 'Wikipedia (en)', 'https://en.wikipedia.org/w/api.php'], 
        ['Emijrp', 'Wikipedia (eo)', 'https://eo.wikipedia.org/w/api.php'], 
        ['Emijrp', 'Wikipedia (es)', 'https://es.wikipedia.org/w/api.php'], 
        ['Emijrp', 'Wikipedia (et)', 'https://et.wikipedia.org/w/api.php'], 
        ['Emijrp', 'Wikipedia (fi)', 'https://fi.wikipedia.org/w/api.php'], 
        ['Emijrp', 'Wikipedia (hu)', 'https://hu.wikipedia.org/w/api.php'], 
        ['Emijrp', 'Wikipedia (it)', 'https://it.wikipedia.org/w/api.php'], 
        ['Emijrp', 'Wikipedia (ja)', 'https://ja.wikipedia.org/w/api.php'], 
        ['Emijrp', 'Wikipedia (fr)', 'https://fr.wikipedia.org/w/api.php'], 
        ['Emijrp', 'Wikipedia (nl)', 'https://nl.wikipedia.org/w/api.php'], 
        ['Emijrp', 'Wikipedia (no)', 'https://no.wikipedia.org/w/api.php'], 
        ['Emijrp', 'Wikipedia (pl)', 'https://pl.wikipedia.org/w/api.php'], 
        ['Emijrp', 'Wikipedia (pt)', 'https://pt.wikipedia.org/w/api.php'], 
        ['Emijrp', 'Wikipedia (ru)', 'https://ru.wikipedia.org/w/api.php'], 
        ['Emijrp', 'Wikipedia (sv)', 'https://sv.wikipedia.org/w/api.php'], 
        ['Emijrp', 'Wikipedia (zh)', 'https://zh.wikipedia.org/w/api.php'], 
        ['Emijrp', 'Wikiquote (en)', 'https://en.wikiquote.org/w/api.php'], 
        ['Emijrp', 'Wikiquote (es)', 'https://es.wikiquote.org/w/api.php'], 
        ['Emijrp', 'Wikisource (en)', 'https://en.wikisource.org/w/api.php'], 
        ['Emijrp', 'Wikisource (es)', 'https://es.wikisource.org/w/api.php'], 
        ['Emijrp', 'Wikispecies', 'https://species.wikimedia.org/w/api.php'], 
        ['Emijrp', 'Wikitech', 'https://wikitech.wikimedia.org/w/api.php'], 
        ['Emijrp', 'Wikiversity (en)', 'https://en.wikiversity.org/w/api.php'], 
        ['Emijrp', 'Wikiversity (es)', 'https://es.wikiversity.org/w/api.php'], 
        ['Emijrp', 'Wikivoyage (en)', 'https://en.wikivoyage.org/w/api.php'], 
        ['Emijrp', 'Wikivoyage (es)', 'https://es.wikivoyage.org/w/api.php'], 
        ['Emijrp', 'Wiktionary (en)', 'https://en.wiktionary.org/w/api.php'], 
        ['Emijrp', 'Wiktionary (es)', 'https://es.wiktionary.org/w/api.php'], 
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

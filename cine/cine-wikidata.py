#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2018 emijrp <emijrp@gmail.com>
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
import time
import urllib2

import cine

def getURL(url=''):
    raw = ''
    if url:
        try:
            req = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
            raw = unicode(urllib2.urlopen(req).read(), 'utf-8')
        except:
            pass
    return raw

def main():
    validp31 = [
        'Q11424', #película
        'Q93204', #cine documental
        'Q24862', #cortometraje
    ]
    url = 'https://xtools.wmflabs.org/api/user/pages/www.wikidata.org/Emijrp'
    json1 = json.loads(getURL(url))
    items = {}
    for page in json1['pages']:
        q = page['page_title']
        qurl = 'https://www.wikidata.org/wiki/Special:EntityData/%s.json' % (q)
        try:
            jsonq = json.loads(getURL(qurl))
        except:
            continue
        if not q in jsonq['entities']:
            continue
        labels = {}
        if 'labels' in jsonq['entities'][q]:
            labels = jsonq['entities'][q]['labels'] 
        claims = {}
        if 'claims' in jsonq['entities'][q]:
            claims = jsonq['entities'][q]['claims']
            if 'P31' in claims:
                p31 = claims['P31']
                if not p31[0]['mainsnak']['datavalue']['value']['id'] in validp31:
                    continue
            else:
                continue
        else:
            continue
        
        items[q] = {
            'q': q, 
            'len': page['page_len'], 
            'creation': page['human_time'], 
            'label-es': 'es' in labels and labels['es']['value'] or u'Título desconocido', 
            'fa': 'P480' in claims and claims['P480'][0]['mainsnak']['datavalue']['value'] or '-', 
            'imdb': 'P345' in claims and claims['P345'][0]['mainsnak']['datavalue']['value'] or '-',  
            'tmdb': 'P4947' in claims and claims['P4947'][0]['mainsnak']['datavalue']['value'] or '-', 
        }
        print(items[q]['q'], items[q]['label-es'], items[q]['fa'])
        time.sleep(0.1)
        #break
    
    table = u'<table class="wikitable sortable" style="text-align: center;">\n'
    table += u"""<tr>
    <th class="sorttable_numeric">#</th>
    <th class="sorttable_alpha">Título</th>
    <th class="sorttable_numeric">FilmAffinity</th>
    <th class="sorttable_numeric">IMDb</th>
    <th class="sorttable_numeric">TMDb</th>
    <th class="sorttable_alpha">Buscadores</th>
</tr>\n"""
    c = 1
    items_list = [[item['label-es'], item] for q, item in items.items()]
    items_list.sort()
    for title, item in items_list:
        title_ = re.sub(' ', '+', title.lower())
        title_ = '%%22%s%%22' % (title_)
        row = u"<tr><td>%s</td><td><i>[https://www.wikidata.org/wiki/%s %s]</i></td><td>[https://www.filmaffinity.com/es/film%s.html %s]</td><td>[https://www.imdb.com/title/%s/ %s]</td><td>[https://www.themoviedb.org/movie/%s %s]</td><td>[https://duckduckgo.com/?q=%s D]{{o}} [https://www.google.es/search?q=%s G]{{o}} [https://www.youtube.com/results?search_query=%s Y]</td></tr>\n" % (c, item['q'], item['label-es'], item['fa'], item['fa'], item['imdb'], item['imdb'], item['tmdb'], item['tmdb'], title_, title_, title_)
        table += row
        c += 1
    table += u'</table>'
    cine.savetable('cine-wikidata.wiki', 'matrixids', table)

if __name__ == '__main__':
    main()

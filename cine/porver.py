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

import datetime
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
    #films watched
    userid = 397713
    filmswatched = []
    for page in range(1, 200):
        faurl = 'https://www.filmaffinity.com/es/userratings.php?user_id=%s&p=%s&orderby=4' % (userid, page)
        print 'Retrieving', faurl
        raw = getURL(url=faurl)
        if not raw:
            break
        m = re.finditer(ur'(?im)<div class="mc-title">\s*<a\s*href="/es/film(?P<id>\d+)\.html"[^<>]*?>', raw)
        for i in m:
            filmswatched.append(i.group('id').strip())
        time.sleep(3)
    
    #films to watch
    topics = ['origins', 'mylist', ]
    filmstowatchfeed = {
        'origins': ['https://www.filmaffinity.com/es/advsearch.php?page=%s&stype[]=title&toyear=1905' % (page) for page in range(1, 100)], #cada pag tiene 25 films
        'mylist': ['https://www.filmaffinity.com/es/userlist.php?user_id=397713&list_id=201&page=%s' % (page) for page in range(1, 20)], #cada pag tiene 50 films
    }
    filmstowatch = {
        'origins': [],
        'mylist': [],
    }
    for topic in topics:
        faurls = filmstowatchfeed[topic]
        for faurl in faurls:
            print 'Retrieving', faurl
            raw = getURL(url=faurl)
            if not raw:
                break
            m = re.finditer(ur'(?im)<div class="mc-title">\s*<a\s*href="/es/film(?P<id>\d+)\.html"[^<>]*?>', raw)
            for i in m:
                filmstowatch[topic].append(i.group('id').strip())
            time.sleep(3)
    
    rows = {
        'origins': [], 
        'mylist': [], 
    }
    for topic in topics:
        for filmtowatch in filmstowatch[topic]:
            faurl = "https://www.filmaffinity.com/es/film%s.html" % (filmtowatch)
            if filmtowatch in filmswatched:
                print "Watched %s" % faurl
            else:
                print "To watch %s" % faurl
                try:
                    raw = getURL(url=faurl)
                    title = re.findall(ur'(?im)<h1 id="main-title">\s*<span itemprop="name">([^<>]*?)</span>\s*</h1>', raw)[0]
                    duration = re.findall(ur'(?im)<dd itemprop="duration">(\d+) min\.</dd>', raw)
                    duration = duration and duration[0] or '?'
                    videos = re.search(ur'Tráilers', raw) and True or False
                    directors = re.findall(ur'(?im)title="([^<>]+?)">', raw.split('<dd class="directors">')[1].split('</dd>')[0])
                    country = re.findall(ur'<dd><span id="country-img"><img src="/imgs/countries/.+jpg" alt="[^<>]+" title="([^<>]+)"></span>[^<>]+</dd>', raw)
                    country = country and country[0] or '?'
                    year = re.findall(ur'<dd itemprop="datePublished">(\d\d\d\d)</dd>', raw)
                    year = year and year[0] or '?'
                    row = [filmtowatch, title, country, year, directors, duration, videos, faurl]
                    print row
                    rows[topic].append(row)
                except:
                    print 'Error'
                    pass
                time.sleep(1.5)
    
    for topic in topics:
        table = u'<table class="wikitable sortable" style="text-align: center;">\n'
        table += u"""<tr>
        <th class="sorttable_numeric">#</th>
        <th class="sorttable_alpha">Título</th>
        <th class="sorttable_alpha">Dirección</th>
        <th class="sorttable_numeric">Año</th>
        <th class="sorttable_alpha">País</th>
        <th class="sorttable_numeric">Duración</th>
        <th class="sorttable_alpha">Vídeos</th>
    </tr>\n"""
        c = 1
        for row in rows[topic]:
            filmtowatch, title, country, year, directors, duration, videos, faurl = row
            if videos:
                rowplain = u"<tr><td>%s</td><td><i>[%s %s]</i></td><td>%s</td><td>%s</td><td>%s</td><td>%s minutos</td><td>[https://www.filmaffinity.com/es/evideos.php?movie_id=%s Sí]</td></tr>\n" % (c, faurl, title, '<br/>'.join(directors), year, country, duration, filmtowatch)
            else:
                rowplain = u"<tr><td>%s</td><td><i>[%s %s]</i></td><td>%s</td><td>%s</td><td>%s</td><td>%s minutos</td><td>No</td></tr>\n" % (c, faurl, title, '<br/>'.join(directors), year, country, duration)
            table += rowplain
            c += 1
        table += u'</table>'
        cine.savetable('porver.wiki', 'porver-%s' % (topic), table)

if __name__ == '__main__':
    main()

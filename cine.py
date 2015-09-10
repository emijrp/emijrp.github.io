#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2015 emijrp <emijrp@gmail.com>
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

import re
import time
import urllib2

def main():
    films = []
    
    for page in range(1, 100):
        faurl = 'http://www.filmaffinity.com/es/userratings.php?user_id=397713&p=%s&orderby=4' % (page)
        
        print 'Retrieving', faurl
        
        try:
            req = urllib2.Request(faurl, headers={ 'User-Agent': 'Mozilla/5.0' })
            html = urllib2.urlopen(req).read()
        except:
            break
        
        #print html
        m = re.findall(ur'(?im)<div class="ur-mr-rat">(\d+)</div>', html)
        ratings = []
        for rating in m:
            ratings.append(rating)
        
        m = re.findall(ur'(?im)<div class="mc-title">\s*<a href="/es/film(\d+)\.html">([^<>]*?)</a>\s*\((\d+?)\)\s*<img src="/imgs/countries/[^<>]+\.jpg" title="([^<>]+?)">\s*</div>\s*<div class="mc-director">\s*<a href="/es/search\.php\?stype=director&amp;sn&amp;stext=[^<>]+?">([^<>]+?)</a></div>', html)
        c = 0
        for film in m:
            filmid = film[0].strip()
            filmtitle = film[1].strip()
            filmyear = film[2].strip()
            filmcountry = film[3].strip()
            filmdirector = film[4].strip()
            films.append([filmtitle, filmyear, filmcountry, filmdirector, filmid, ratings[c]])
            c += 1
        
        time.sleep(1)
    
    films.sort()
    
    rows = []
    for film in films:
        filmtitle = film[0]
        filmyear = film[1]
        filmcountry = film[2]
        filmdirector = film[3]
        filmid = film[4]
        filmrating = film[5]
        
        if 'Serie de TV' in filmtitle or '(C)' in filmtitle:
            continue
        
        if filmtitle.endswith(' (TV)'):
            filmtitle = filmtitle.split(' (TV)')[0]
        
        if 'AKA' in filmdirector:
            filmdirector = filmdirector.split(' (AKA')[0]
        
        if 'URSS' in filmcountry:
            filmcountry = filmcountry.split(' (URSS)')[0]
        
        row = '<tr><td><i><a href="http://www.filmaffinity.com/es/film%s.html">%s</a></i></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>\n' % (filmid, filmtitle, filmdirector, filmyear, filmcountry, filmrating)
        rows.append(row)
    
    table = '\n<table class="wikitable sortable" style="text-align: center;">\n'
    table += '<tr><th>Título</th><th>Dirección</th><th>Año</th><th>País</th><th>Puntos</th></tr>'
    table += ''.join(rows)
    table += '</table>\n'
    
    f = open('cine.html', 'r')
    html = f.read()
    f.close()
    f = open('cine.html', 'w')
    html = html.split('<!-- tabla completa -->')[0] + '<!-- tabla completa -->' + table + '<!-- /tabla completa -->' + html.split('<!-- /tabla completa -->')[1]
    f.write(html)
    f.close()

if __name__ == '__main__':
    main()

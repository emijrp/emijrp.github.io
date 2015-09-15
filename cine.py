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
    countries = {
        u'Unión Soviética': u'ZY', 
    }
    userid = 397713
    
    for page in range(1, 100):
        faurl = 'http://www.filmaffinity.com/es/userratings.php?user_id=%s&p=%s&orderby=4' % (userid, page)
        
        print 'Retrieving', faurl
        
        try:
            req = urllib2.Request(faurl, headers={ 'User-Agent': 'Mozilla/5.0' })
            html = unicode(urllib2.urlopen(req).read(), 'utf-8')
        except:
            break
        
        #print html
        m = re.findall(ur'(?im)<div class="ur-mr-rat">(\d+)</div>', html)
        ratings = []
        for rating in m:
            ratings.append(rating)
        
        m = re.findall(ur'(?im)<div class="mc-title">\s*<a href="/es/film(\d+)\.html">([^<>]*?)</a>\s*\((\d+?)\)\s*<img src="/imgs/countries/([^<>]+)\.jpg" title="([^<>]+?)">\s*</div>\s*<div class="mc-director">\s*<a href="/es/search\.php\?stype=director&amp;sn&amp;stext=[^<>]+?">([^<>]+?)</a>', html) #no cerrar con </div> por si el campo director tiene más de un director
        c = 0
        for film in m:
            filmid = film[0].strip()
            filmtitle = film[1].strip()
            filmyear = int(film[2].strip())
            filmcountryid = film[3].strip()
            filmcountry = film[4].strip()
            filmdirector = film[5].strip()
            films.append([filmtitle, filmyear, filmcountry, filmdirector, filmid, ratings[c]])
            countries[filmcountry] = filmcountryid
            c += 1
        
        time.sleep(1)
    
    films.sort()
    
    rows = []
    c = 0
    for film in films:
        filmtitle = film[0]
        filmyear = film[1]
        filmcountry = film[2]
        filmdirector = film[3]
        filmid = film[4]
        filmrating = film[5]
        
        customkey = re.sub(ur'(?im)[\"\!\¡\?\¿\#]', '', filmtitle)
        
        if 'Serie de TV' in filmtitle:# or '(C)' in filmtitle:
            continue
        
        if filmtitle.endswith(' (TV)'):
            filmtitle = filmtitle.split(' (TV)')[0]
        
        if '(AKA' in filmdirector:
            filmdirector = filmdirector.split(' (AKA')[0]
        if '(Creator' in filmdirector:
            filmdirector = filmdirector.split(' (Creator')[0]
        
        if 'URSS' in filmcountry:
            filmcountry = filmcountry.split(' (URSS)')[0]
        
        c += 1
        filmdirectorlink = 'http://www.filmaffinity.com/es/search.php?stype=director&sn&stext=%s' % (re.sub(' ', '+', filmdirector))
        if filmyear < 1900:
            filmyearlink = 'http://www.filmaffinity.com/es/advsearch.php?stext=&stype[]=title&country=&genre=&fromyear=&toyear=1900'
        else:
            filmyearlink = 'http://www.filmaffinity.com/es/advsearch.php?stext=&stype[]=title&country=&genre=&fromyear=%s&toyear=%s' % (filmyear, filmyear)
        row = u"""
    <tr>
        <td>%s</td>
        <td sorttable_customkey="%s"><i><a href="http://www.filmaffinity.com/es/film%s.html">%s</a></i></td>
        <td><a href="%s">%s</a></td>
        <td><a href="%s">%s</a></td>
        <td><a href="http://www.filmaffinity.com/es/advsearch.php?stext=&stype[]=title&country=%s&genre=&fromyear=&toyear=">%s</a></td>
        <td>%s</td>
    </tr>\n""" % (c, customkey, filmid, filmtitle, filmdirectorlink, filmdirector, filmyearlink, filmyear, countries[filmcountry], filmcountry, filmrating)
        rows.append(row)
    
    table = u"\n<script>sorttable.sort_alpha = function(a,b) { return a[0].localeCompare(b[0], 'es'); }</script>\n"
    table += u'\n<table class="wikitable sortable" style="text-align: center;">\n'
    table += u"""
    <tr>
        <th class="sorttable_numeric">#</th>
        <th class="sorttable_alpha">Título</th>
        <th class="sorttable_alpha">Dirección</th>
        <th class="sorttable_numeric">Año</th>
        <th class="sorttable_alpha">País</th>
        <th class="sorttable_numeric">Puntos</th>
    </tr>"""
    table += u''.join(rows)
    table += u'</table>\n'
    
    f = open('cine.html', 'r')
    html = unicode(f.read(), 'utf-8')
    f.close()
    f = open('cine.html', 'w')
    html = u'%s<!-- tabla completa -->%s<!-- /tabla completa -->%s' % (html.split(u'<!-- tabla completa -->')[0], table, html.split(u'<!-- /tabla completa -->')[1])
    f.write(html.encode('utf-8'))
    f.close()

if __name__ == '__main__':
    main()

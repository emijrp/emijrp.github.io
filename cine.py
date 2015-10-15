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

import datetime
import re
import time
import urllib2

countries = {
    u'Unión Soviética': u'ZY', 
}

def cleanFilmDirector(filmdirector):
    if '(AKA' in filmdirector:
        filmdirector = filmdirector.split(' (AKA')[0]
    if '(Creator' in filmdirector:
        filmdirector = filmdirector.split(' (Creator')[0]
    return filmdirector

def getFilmCountryLink(filmcountry):
    filmcountrylink = 'http://www.filmaffinity.com/es/advsearch.php?stext=&stype[]=title&country=%s&genre=&fromyear=&toyear=' % (countries[filmcountry])
    return filmcountrylink
    
def getFilmDirectorLink(filmdirector):
    return 'http://www.filmaffinity.com/es/search.php?stype=director&sn&stext=%s' % (re.sub(' ', '+', filmdirector))

def getFilmYearLink(filmyear):
    filmyearlink = ''
    if filmyear < 1900:
        filmyearlink = 'http://www.filmaffinity.com/es/advsearch.php?stext=&stype[]=title&country=&genre=&fromyear=&toyear=1900'
    else:
        filmyearlink = 'http://www.filmaffinity.com/es/advsearch.php?stext=&stype[]=title&country=&genre=&fromyear=%s&toyear=%s' % (filmyear, filmyear)
    return filmyearlink    

def main():
    films = []
    
    userid = 397713
    
    #stats
    statsdirector = {}
    statscountry = {}
    statsyear = {}
    statsdecade = {}
    
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
        
        m = re.findall(ur'(?im)<div class="mc-title">\s*<a href="/es/film(\d+)\.html">([^<>]*?)</a>\s*\((\d+?)\)\s*<img src="/imgs/countries/([^<>]+)\.jpg" title="([^<>]+?)">\s*</div>\s*<div class="mc-director">\s*<a href="/es/search\.php\?stype=director&amp;sn&amp;stext=[^<>]+?">([^<>]+?)</a>', html) #no cerrar con </div> por si el campo director tiene más de un director, solo coge el primero (mejorar?)
        c = 0
        for film in m:
            filmid = film[0].strip()
            filmtitle = film[1].strip()
            filmyear = int(film[2].strip())
            filmdecade = filmyear / 10
            filmcountryid = film[3].strip()
            filmcountry = film[4].strip()
            filmdirector = film[5].strip()
            films.append([filmtitle, filmyear, filmcountry, filmdirector, filmid, ratings[c]])
            countries[filmcountry] = filmcountryid
            
            statsyear[filmyear] = statsyear.has_key(filmyear) and statsyear[filmyear] + 1 or 1
            statsdecade[filmdecade] = statsdecade.has_key(filmdecade) and statsdecade[filmdecade] + 1 or 1
            statscountry[filmcountry] = statscountry.has_key(filmcountry) and statscountry[filmcountry] + 1 or 1
            statsdirector[filmdirector] = statsdirector.has_key(filmdirector) and statsdirector[filmdirector] + 1 or 1

            c += 1
        
        time.sleep(1)
    
    films.sort()
    
    rows = []
    years = set([])
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
        
        filmdirector_ = cleanFilmDirector(filmdirector)
        
        if 'Holanda' in filmcountry:
            filmcountry = filmcountry.split(' (Holanda)')[0]
        if 'URSS' in filmcountry:
            filmcountry = filmcountry.split(' (URSS)')[0]
        
        years.add(filmyear)
        c += 1
        filmcountrylink = getFilmCountryLink(filmcountry)
        filmdirectorlink = getFilmDirectorLink(filmdirector)
        filmyearlink = getFilmYearLink(filmyear)
        row = u"""
    <tr>
        <td>%s</td>
        <td sorttable_customkey="%s"><i><a href="http://www.filmaffinity.com/es/film%s.html">%s</a></i></td>
        <td><a href="%s">%s</a></td>
        <td><a href="%s">%s</a></td>
        <td><a href="%s">%s</a></td>
        <td>%s</td>
    </tr>\n""" % (c, customkey, filmid, filmtitle, filmdirectorlink, filmdirector_, filmyearlink, filmyear, filmcountrylink, filmcountry, filmrating)
        rows.append(row)
    
    #add missing years
    for i in range(1890, datetime.datetime.now().year+1):
        if i not in years:
            row = u"""
    <tr>
        <td>-</td>
        <td sorttable_customkey="-"><i>Ninguna del año %s</i></td>
        <td>-</td>
        <td><a href="%s">%s</a></td>
        <td>-</td>
        <td>-</td>
    </tr>\n""" % (i, getFilmYearLink(i), i)
            rows.append(row)
    
    #add missing countries
    countriesurl = 'http://www.filmaffinity.com/es/advsearch.php'
    try:
        req2 = urllib2.Request(countriesurl, headers={ 'User-Agent': 'Mozilla/5.0' })
        html2 = unicode(urllib2.urlopen(req2).read(), 'utf-8')
    except:
        print 'ERROR: countries'
        sys.exit()
    
    html2 = html2.split('<select name="country">')[1]
    html2 = html2.split('</select>')[0]
    allcountries = re.findall(ur'(?im)<option value="([^<>]+?)">([^<>]+?)</option>', html2)
    for x, y in allcountries:
        if x not in countries.values():
            row = u"""
    <tr>
        <td>-</td>
        <td sorttable_customkey="-"><i>Ninguna de %s</i></td>
        <td>-</td>
        <td sorttable_customkey="2099">-</td>
        <td><a href="http://www.filmaffinity.com/es/advsearch.php?stext=&stype[]=title&country=%s&genre=&fromyear=&toyear=">%s</a></td>
        <td>-</td>
    </tr>\n""" % (y, x, y)
            rows.append(row)
    
    #print table
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
    
    #print stats
    statsyear_list = [[y, x] for x, y in statsyear.items()]
    statsyear_list.sort()
    statsyear_list.reverse()
    
    statsdecade_list = [[y, x] for x, y in statsdecade.items()]
    statsdecade_list.sort()
    statsdecade_list.reverse()
    
    statsdirector_list = [[y, x] for x, y in statsdirector.items()]
    statsdirector_list.sort()
    statsdirector_list.reverse()
    
    statscountry_list = [[y, x] for x, y in statscountry.items()]
    statscountry_list.sort()
    statscountry_list.reverse()
    
    stats = u"<ul>\n"
    stats += u"<li>Por <b>años</b>: %s</a>\n" % (', '.join([u'<a href="%s">%s</a> (%s)' % (getFilmYearLink(x), x, y) for y, x in statsyear_list]))
    stats += u"<li>Por <b>décadas</b>: %s</a>\n" % (', '.join([u'%s0 (%s)' % (x, y) for y, x in statsdecade_list]))
    stats += u"<li>Por <b>director</b>: %s</a>\n" % (', '.join([u'<a href="%s">%s</a> (%s)' % (getFilmDirectorLink(x), cleanFilmDirector(x), y) for y, x in statsdirector_list]))
    stats += u"<li>Por <b>país</b>: %s</a>\n" % (', '.join([u'<a href="%s">%s</a> (%s)' % (getFilmCountryLink(x), x, y) for y, x in statscountry_list]))
    stats += u"</ul>\n"
    
    f = open('cine.html', 'r')
    html = unicode(f.read(), 'utf-8')
    f.close()
    f = open('cine.html', 'w')
    html = u'%s<!-- stats -->%s<!-- /stats -->%s' % (html.split(u'<!-- stats -->')[0], stats, html.split(u'<!-- /stats -->')[1])
    f.write(html.encode('utf-8'))
    f.close()

if __name__ == '__main__':
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2015-2016 emijrp <emijrp@gmail.com>
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
import urllib
import urllib2

country2id = {
    u'Unión Soviética': u'ZY', 
}

def cleanFilmCountry(filmcountry):
    filmcountry = filmcountry.strip()
    if 'Holanda' in filmcountry:
        filmcountry = filmcountry.split(' (Holanda)')[0]
    if 'URSS' in filmcountry:
        filmcountry = filmcountry.split(' (URSS)')[0]
    return filmcountry

def cleanFilmDirector(filmdirector):
    filmdirector = filmdirector.strip()
    if '(AKA' in filmdirector:
        filmdirector = filmdirector.split(' (AKA')[0]
    if '(Creator' in filmdirector:
        filmdirector = filmdirector.split(' (Creator')[0]
    return filmdirector

def getFilmCountryLink(filmcountry):
    filmcountry = filmcountry.strip()
    filmcountrylink = 'http://www.filmaffinity.com/es/advsearch.php?stext=&stype[]=title&country=%s&genre=&fromyear=&toyear=' % (country2id[filmcountry])
    return filmcountrylink
    
def getFilmDirectorLink(filmdirector):
    filmdirector = filmdirector.strip()
    return 'http://www.filmaffinity.com/es/search.php?stype=director&sn&stext=%s' % (re.sub(' ', '+', filmdirector))

def getFilmYearLink(filmyear):
    filmyearlink = ''
    if filmyear < 1900:
        filmyearlink = 'http://www.filmaffinity.com/es/advsearch.php?stext=&stype[]=title&country=&genre=&fromyear=&toyear=1900'
    else:
        filmyearlink = 'http://www.filmaffinity.com/es/advsearch.php?stext=&stype[]=title&country=&genre=&fromyear=%s&toyear=%s' % (filmyear, filmyear)
    return filmyearlink    

def savetable(filename, tablemark, table):
    f = open(filename, 'r')
    html = unicode(f.read(), 'utf-8')
    f.close()
    f = open(filename, 'w')
    before = html.split(u'<!-- %s -->' % tablemark)[0]
    after = html.split(u'<!-- /%s -->' % tablemark)[1]
    html = u'%s<!-- %s -->%s<!-- /%s -->%s' % (before, tablemark, table, tablemark, after)
    f.write(html.encode('utf-8'))
    f.close()

def main():
    films = []
    films2watch = []
    userid = 397713
    
    #stats
    statsdirector = {}
    statscountry = {}
    statsyear = {}
    statsdecade = {}
    
    """
    #read 15mpedia pages, lo comento porque la mayoría de pelis no tiene cabida en el wiki, habría que enfocarlo de otra forma esto
    pediafilms = {}
    startid = u'-'
    while startid:
        print startid
        print 'Reading 15Mpedia films from %s' % startid
        queryurl = u'https://15mpedia.org/w/index.php?title=Especial%%3AAsk&q=[[Page+has+default+form%%3A%%3APelícula]][[filmaffinity+id%%3A%%3A!no]][[filmaffinity+id%%3A%%3A%%3E%s]]&p=format%%3Dbroadtable%%2Flink%%3Dall%%2Fheaders%%3Dshow%%2Fclass%%3Dsortable-20wikitable-20smwtable&po=%%3FFilmaffinity+id%%0A%%3FRebeldemule+url%%0A%%3FVimeo+id%%0A%%3FYoutube+id%%0A&eq=yes' % (startid)
        try:
            req = urllib2.Request(queryurl.encode('utf-8'), headers={ 'User-Agent': 'Mozilla/5.0' })
            html = unicode(urllib2.urlopen(req).read(), 'utf-8')
        except:
            break
        #print html
        m = re.findall(ur'(?im)<tr class="row-(?:even|odd)">\s*<td[^<>]*?><a href=[^<>]*?>([^<>]*?)</a></td>\s*<td[^<>]*?>([^<>]*?)</td>\s*<td[^<>]*?>(?:<a [^<>]*?>([^<>]*?)</a>|)</td>\s*<td[^<>]*?>([^<>]*?)</td>\s*<td[^<>]*?>([^<>]*?)</td>\s*</tr>', html)
        if len(m) > 0:
            for i in m:
                pediafilms[i[1]] = {'title':i[0], 'fa':i[1], 'rm':i[2], 'vimeo':i[3], 'youtube':i[4]}
            if startid == i[1]:
                break
            else:
                startid = i[1]
        else:
            print 'La regexp fallo'
            sys.exit()
    #print pediafilms.items()
    """
    
    #read filmaffinity profile
    ratings = []
    for page in range(1, 100):
        faurl = 'https://www.filmaffinity.com/es/userratings.php?user_id=%s&p=%s&orderby=4' % (userid, page)
        print 'Retrieving', faurl
        try:
            req = urllib2.Request(faurl, headers={ 'User-Agent': 'Mozilla/5.0' })
            html = unicode(urllib2.urlopen(req).read(), 'utf-8')
        except:
            break
        
        #print html
        m = re.findall(ur'(?im)<div class="ur-mr-rat">(\d+)</div>', html)
        del ratings[:]
        for rating in m:
            ratings.append(rating)
        #print('Ratings',len(ratings))
        
        m = re.finditer(ur'(?im)<div class="mc-title">\s*<a\s*href="/es/film(?P<id>\d+)\.html"[^<>]*?>(?P<title>[^<>]*?)</a>\s*\((?P<year>\d\d\d\d)\)\s*<img src="/imgs/countries/(?P<countryid>[^<>]+)\.jpg" [^<>]*?title="(?P<country>[^<>]+?)">\s*</div>\s*<div class="mc-director">\s*(<div class="credits">)?\s*(?P<director>(\s*(<span class="nb">)?\s*[^<>]*?<a[^<>]*?>[^<>]*?</a>[^<>]*?(</span>)?\s*)*?)[^<>]*?(</div>)?[^<>]*?</div>[^<>]*?<div class="mc-cast">\s*(<div class="credits">)?\s*(?P<cast>(\s*(<span class="nb">)?\s*[^<>]*?<a[^<>]*?>[^<>]*?</a>[^<>]*?(</span>)?\s*)*?)[^<>]*?(</div>)?[^<>]*?</div>', html)
        c = 0 #for ratings index
        for i in m:
            filmprops = {}
            filmprops['id'] = i.group('id').strip()
            filmprops['title'] = i.group('title').strip()
            #print filmprops['title']
            filmprops['year'] = int(i.group('year').strip())
            filmprops['decade'] = filmprops['year'] / 10
            filmprops['countryid'] = i.group('countryid').strip()
            filmprops['country'] = i.group('country').strip()
            filmprops['director'] = re.findall(ur'(?im)<a[^<>]+?>([^<>]*?)</a>', i.group('director').strip())
            filmprops['cast'] = i.group('cast').strip()
            filmprops['rating'] = ratings[c]
            films.append([filmprops['title'], filmprops])
            country2id[filmprops['country']] = filmprops['countryid']
            
            if not 'Documentary' in filmprops['cast'] and not 'Serie de TV' in filmprops['title']:
                statsyear[filmprops['year']] = statsyear.has_key(filmprops['year']) and statsyear[filmprops['year']] + 1 or 1
                statsdecade[filmprops['decade']] = statsdecade.has_key(filmprops['decade']) and statsdecade[filmprops['decade']] + 1 or 1
                statscountry[filmprops['country']] = statscountry.has_key(filmprops['country']) and statscountry[filmprops['country']] + 1 or 1
                for director in filmprops['director']:
                    statsdirector[director] = statsdirector.has_key(director) and statsdirector[director] + 1 or 1
            c += 1
        if (c != 30 or len(ratings) != 30) and not 'El acorazado Potemkin' in html:
            print 'ERROR al capturar los datos'
            sys.exit()
        time.sleep(1)
    films.sort()
    print('%d films' % len(films))
    
    #read films to watch
    for page in range(1, 100):
        faurl = 'https://www.filmaffinity.com/es/userlist.php?user_id=%s&list_id=201&page=%s&orderby=0' % (userid, page)
        print 'Retrieving', faurl
        try:
            req = urllib2.Request(faurl, headers={ 'User-Agent': 'Mozilla/5.0' })
            html = unicode(urllib2.urlopen(req).read(), 'utf-8')
        except:
            break
        
        m = re.finditer(ur'(?im)<div class="mc-title">\s*<a\s*href="/es/film(?P<id>\d+)\.html"[^<>]*?>(?P<title>[^<>]*?)</a>\s*\((?P<year>\d+?)\)\s*<img src="/imgs/countries/(?P<countryid>[^<>]+)\.jpg" [^<>]*?title="(?P<country>[^<>]+?)">\s*</div>', html)
        for i in m:
            filmprops = {}
            filmprops['id'] = i.group('id').strip()
            filmprops['title'] = i.group('title').strip()
            filmprops['year'] = int(i.group('year').strip())
            filmprops['countryid'] = i.group('countryid').strip()
            filmprops['country'] = i.group('country').strip()
            films2watch.append([filmprops['title'], filmprops])
            country2id[filmprops['country']] = filmprops['countryid']
        time.sleep(1)
    films2watch.sort()
    print('%d films to watch' % len(films2watch))
    
    #generate table
    filmrows = []
    docrows = []
    seriesrows = []
    years = set([])
    countries = set([])
    filmc = 0
    docc = 0
    seriesc = 0
    for filmtitle, filmprops in films:
        filmtitle_ = filmtitle
        if filmtitle_.endswith(' (TV)'):
            filmtitle_ = filmtitle_.split(' (TV)')[0]
        
        customkey = re.sub(ur'(?im)[\"\!\¡\?\¿\#]', '', filmtitle_)
        director_ = []
        [director_.append(cleanFilmDirector(director)) for director in filmprops['director']]
        country = cleanFilmCountry(filmprops['country'])
        countrylink = getFilmCountryLink(filmprops['country'])
        directorlink = [getFilmDirectorLink(director) for director in filmprops['director']]
        yearlink = getFilmYearLink(filmprops['year'])
        directors = []
        for d in range(0, len(director_)):
            directors.append('<a href="%s">%s</a>' % (directorlink[d], director_[d]))
        directors = '<br/>'.join(directors)
        if 'Documentary' in filmprops['cast']:
            filmtitle_ = filmtitle_.split(' (Serie de TV)')[0] # some documentaries include (Serie de TV) suffix
            docc += 1
            row = u"""
    <tr>
        <td>%s</td>
        <td sorttable_customkey="%s"><i><a href="http://www.filmaffinity.com/es/film%s.html">%s</a></i></td>
        <td>%s</td>
        <td><a href="%s">%s</a></td>
        <td><a href="%s">%s</a></td>
        <td>%s</td>
    </tr>\n""" % (docc, customkey, filmprops['id'], filmtitle_, directors, yearlink, filmprops['year'], countrylink, country, filmprops['rating'])
            docrows.append(row)
        elif 'Serie de TV' in filmtitle_:
            filmtitle_ = filmtitle_.split(' (Serie de TV)')[0]
            seriesc += 1
            row = u"""
    <tr>
        <td>%s</td>
        <td sorttable_customkey="%s"><i><a href="http://www.filmaffinity.com/es/film%s.html">%s</a></i></td>
        <td>%s</td>
        <td><a href="%s">%s</a></td>
        <td><a href="%s">%s</a></td>
        <td>%s</td>
    </tr>\n""" % (seriesc, customkey, filmprops['id'], filmtitle_, directors, yearlink, filmprops['year'], countrylink, country, filmprops['rating'])
            seriesrows.append(row)
        else:
            filmc += 1
            years.add(filmprops['year'])
            countries.add(filmprops['countryid'])
            row = u"""
    <tr>
        <td>%s</td>
        <td sorttable_customkey="%s"><i><a href="http://www.filmaffinity.com/es/film%s.html">%s</a></i></td>
        <td>%s</td>
        <td><a href="%s">%s</a></td>
        <td><a href="%s">%s</a></td>
        <td>%s</td>
    </tr>\n""" % (filmc, customkey, filmprops['id'], filmtitle_, directors, yearlink, filmprops['year'], countrylink, country, filmprops['rating'])
            filmrows.append(row)
    
    #add missing years
    for i in range(1900, datetime.datetime.now().year+1):
        if i not in years:
            suggest = []
            suggest_plain = u""
            for film2watchtitle, film2watchprops in films2watch:
                if film2watchprops['year'] == i:
                    suggest.append(u'<i><a href="http://www.filmaffinity.com/es/film%s.html">%s</a></i> (%s)' % (film2watchprops['id'], film2watchprops['title'], cleanFilmCountry(film2watchprops['country'])))
            if suggest:
                suggest_plain = u"<br/><br/>Sugerencias:<br/>%s" % (u'<br/>'.join(suggest))
            row = u"""
    <tr>
        <td sorttable_customkey="ZZZ">-</td>
        <td><i>Ninguna del año %s</i>%s</td>
        <td sorttable_customkey="ZZZ">-</td>
        <td><a href="%s">%s</a></td>
        <td sorttable_customkey="ZZZ">-</td>
        <td sorttable_customkey="ZZZ">-</td>
    </tr>\n""" % (i, suggest_plain, getFilmYearLink(i), i)
            filmrows.append(row)
    
    #add missing countries
    countriesurl = 'http://www.filmaffinity.com/es/advsearch.php'
    try:
        req2 = urllib2.Request(countriesurl, headers={ 'User-Agent': 'Mozilla/5.0' })
        html2 = unicode(urllib2.urlopen(req2).read(), 'utf-8')
    except:
        print 'ERROR: countries'
        sys.exit()
    
    html2 = html2.split('<select name="country" id="country">')[1]
    html2 = html2.split('</select>')[0]
    allcountries = re.findall(ur'(?im)<option value="([^<>]+?)"\s*>([^<>]+?)</option>', html2)
    for x, y in allcountries:
        if x not in countries:
            suggest = []
            suggest_plain = u""
            for film2watchtitle, film2watchprops in films2watch:
                if film2watchprops['countryid'] == x:
                    suggest.append(u'<i><a href="http://www.filmaffinity.com/es/film%s.html">%s</a></i> (%s)' % (film2watchprops['id'], film2watchprops['title'], film2watchprops['year']))
            if suggest:
                suggest_plain = u"<br/><br/>Sugerencias:<br/>%s" % (u'<br/>'.join(suggest))
            row = u"""
    <tr>
        <td sorttable_customkey="ZZZ">-</td>
        <td><i>Ninguna de %s</i>%s</td>
        <td sorttable_customkey="ZZZ">-</td>
        <td sorttable_customkey="2099">-</td>
        <td><a href="http://www.filmaffinity.com/es/advsearch.php?stext=&stype[]=title&country=%s&genre=&fromyear=&toyear=">%s</a></td>
        <td sorttable_customkey="ZZZ">-</td>
    </tr>\n""" % (cleanFilmCountry(y), suggest_plain, x, cleanFilmCountry(y))
            filmrows.append(row)
    
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
    filmtable = table
    filmtable += u''.join(filmrows)
    filmtable += u'</table>\n'
    
    doctable = table
    doctable += u''.join(docrows)
    doctable += u'</table>\n'
    
    seriestable = table
    seriestable += u''.join(seriesrows)
    seriestable += u'</table>\n'
    
    savetable('cine.wiki', 'tabla completa', filmtable)
    savetable('documentales.wiki', 'tabla completa', doctable)
    savetable('series.wiki', 'tabla completa', seriestable)
    
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
    
    savetable('cine.wiki', 'stats', stats)
    
if __name__ == '__main__':
    main()

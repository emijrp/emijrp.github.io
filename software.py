#!/usr/bin/env python
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

import json
import sys
import time
import urllib2

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
    
    # GitHub repos
    ghrepos = []
    for ghpage in range(1,1000):
        ghurl = 'https://api.github.com/users/emijrp/repos?page=%d' % (ghpage)
        print ghurl
        
        try:
            ghreq = urllib2.Request(ghurl, headers={ 'User-Agent': 'Mozilla/5.0' })
            ghhtml = unicode(urllib2.urlopen(ghreq).read(), 'utf-8')
        except:
            sys.exit()
        
        ghjson = json.loads(ghhtml)
        if not ghjson:
            break
        
        for ghrepo in ghjson:
            ghrepos.append([ghrepo['fork'], ghrepo['name'], ghrepo['id'], ghrepo])
        time.sleep(1)
    ghrepos.sort()
    print(len(ghrepos),'GitHub repos')
    
    ghrows = []
    ghc = 1
    for ghfork, ghame, ghrepoid, ghprops in ghrepos:
        ghrow = u"""
    <tr>
        <td>%s</td>
        <td sorttable_customkey="%s"><a href="%s">%s</a></td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
    </tr>\n""" % (ghc, ghprops['name'], ghprops['html_url'], ghprops['name'], ghprops['private'] and u'Privado' or u'Público', ghprops['fork'] and u'Sí' or 'No', ghprops['language'], ghprops['size'], ghprops['forks_count'], ghprops['description'], ghprops['stargazers_count'])
        ghrows.append(ghrow)
        ghc += 1
    
    #print table
    ghtable = u"\n<script>sorttable.sort_alpha = function(a,b) { return a[0].localeCompare(b[0], 'es'); }</script>\n"
    ghtable += u'\n<table class="wikitable sortable" style="text-align: center;">\n'
    ghtable += u"""
    <tr>
        <th class="sorttable_numeric">#</th>
        <th class="sorttable_alpha">Nombre</th>
        <th class="sorttable_alpha">Estado</th>
        <th class="sorttable_alpha">¿Fork?</th>
        <th class="sorttable_alpha">Lenguaje</th>
        <th class="sorttable_numeric">Tamaño</th>
        <th class="sorttable_numeric">Forks</th>
        <th class="sorttable_alpha">Descripción</th>
        <th class="sorttable_numeric">Estrellas</th>
    </tr>"""
    ghtable += u''.join(ghrows)
    ghtable += u'</table>\n'
    
    savetable('software.wiki', 'tabla completa github', ghtable)

if __name__ == '__main__':
    main()

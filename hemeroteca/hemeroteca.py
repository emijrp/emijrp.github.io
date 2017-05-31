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

import datetime
import html
import json
import re
import urllib.request

medios = {
    'diariooctubre': { 'nombre': 'Diario Octubre', 'portada': 'https://diario-octubre.com', 'feed': 'https://diario-octubre.com/feed/' }, 
    'elterritoriodellince': { 'nombre': 'El Territorio del Lince', 'portada': 'https://elterritoriodellince.blogspot.com', 'feed': 'https://elterritoriodellince.blogspot.com' }, 
}

def getURL(url=''):
    req = urllib.request.Request(url=url, data=None, headers={ 'User-Agent': 'Mozilla/5.0' })
    f = urllib.request.urlopen(req)
    return f.read().decode('utf-8')

def diariooctubre(medio=''):
    posts = {}
    raw = getURL(url=medios[medio]['feed'])
    xtitles = re.findall(r'<title>([^<>]+?)</title>', raw)
    xposts = re.findall(r"<link>(https?://diario-octubre.com[^ ]+?)</link>", raw)
    xdates = re.findall(r"<pubDate>([^<>]+?)</pubDate>", raw)
    if len(xposts) != len(xdates):
        print('Error en %s' % (medio))
    else:
        c = 1
        while c < len(xposts):
            dt = datetime.datetime.strptime(xdates[c].split(' +')[0], "%a, %d %b %Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")  
            posts[xposts[c]] = { 'medio': medio, 'titulo': html.unescape(xtitles[c]), 'fecha': dt }
            c += 1
    return posts

def elterritoriodellince(medio=''):
    posts = {}
    raw = getURL(url=medios[medio]['feed'])
    xtitles = re.findall(r'<span style="color: red; font-size: large;"><b>([^<>]+?)</b></span>', raw)
    xposts = re.findall(r"<meta content='(https?://elterritoriodellince.blogspot.com[^ ]+?)' itemprop='url'/>", raw)
    xdates = re.findall(r"itemprop='datePublished' title='(\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d)", raw)
    if len(xposts) != len(xdates):
        print('Error en %s' % (medio))
    else:
        c = 0
        while c < len(xposts):
            posts[xposts[c]] = { 'medio': medio, 'titulo': html.unescape(xtitles[c]), 'fecha': re.sub('T', ' ', xdates[c]) }
            c += 1
    return posts

def savetable(filename, tablemark, table):
    f = open(filename, 'r')
    html = f.read()
    f.close()
    f = open(filename, 'w')
    before = html.split(u'<!-- %s -->' % tablemark)[0]
    after = html.split(u'<!-- /%s -->' % tablemark)[1]
    html = u'%s<!-- %s -->%s<!-- /%s -->%s' % (before, tablemark, table, tablemark, after)
    f.write(html)
    f.close()

def main():
    posts = []
    posts.append(diariooctubre(medio='diariooctubre'))
    posts.append(elterritoriodellince(medio='elterritoriodellince'))
    postsall = {}
    for posts2 in posts:
        for k, v in posts2.items():
            postsall[k] = v
    posts = postsall
            
    #print(json.dumps(posts, sort_keys=True))
    with open('hemeroteca.json', 'w') as outfile:
        outfile.write(json.dumps(posts, sort_keys=True))
    
    postslist = []
    for posturl, props in posts.items():
        postslist.append([props['fecha'], props['titulo'], props['medio'], posturl])
    postslist.sort(reverse=True)
    
    output = """<table class="wikitable sortable">
<tr>
    <th>Fecha</th>
    <th>Título</th>
    <th>Medio</th>
</tr>
"""
    for fecha, titulo, medio, url in postslist:
        output += """<tr>
    <td>%s</td>
    <td>[%s %s]</td>
    <td style="text-align: center;">[%s %s]</td>
</tr>""" % (fecha, url, titulo, medios[medio]['portada'], medios[medio]['nombre'])
    output += '\n</table>'
    savetable('hemeroteca.wiki', 'ultimasnoticias', output)
            
if __name__ == '__main__':
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2016-2017 emijrp <emijrp@gmail.com>
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

sites = {
    'diariooctubre': {
        'name': 'Diario Octubre', 
        'mainpage': 'https://diario-octubre.com', 
        'feed': 'https://diario-octubre.com/feed/', 
    }, 
    'elterritoriodellince': {
        'name': 'El Territorio del Lince', 
        'mainpage': 'https://elterritoriodellince.blogspot.com', 
        'feed': 'https://elterritoriodellince.blogspot.com/feeds/posts/default', 
        'logo': 'https://lh5.googleusercontent.com/-agtmdlUWIEg/AAAAAAAAAAI/AAAAAAAAABM/BCj2JvVroTs/s80-c/photo.jpg', 
    }, 
    'labocadora': {
        'name': "La Boca d'Or", 
        'mainpage': 'https://labocadora.blogspot.com', 
        'feed': 'https://labocadora.blogspot.com/feeds/posts/default', 
        'logo': 'https://2.bp.blogspot.com/-n92IvcH0t1c/T6xAHU2Ki3I/AAAAAAAAAA8/7l8TifE0UEs/s113/bocca.jpg', 
    }, 
    'sputniknews': {
        'name': 'Sputnik News', 
        'mainpage': 'https://mundo.sputniknews.com', 
        'feed': 'https://mundo.sputniknews.com/export/rss2/archive/index.xml', 
    }, 
}

def cleancontent(text=''):
    text = re.sub(r"</?[^<>]*?>", r"", text)
    return text

def getURL(url=''):
    req = urllib.request.Request(url=url, data=None, headers={ 'User-Agent': 'Mozilla/5.0' })
    f = urllib.request.urlopen(req)
    return f.read().decode('utf-8')

def diariooctubre(medio=''):
    posts = {}
    raw = getURL(url=medios[medio]['feed'])
    raw = '<item>'.join(raw.split('<item>')[1:])
    xtitles = re.findall(r'<title>([^<>]+?)</title>', raw)
    xurls = re.findall(r"<link>(https?://diario-octubre.com[^ ]+?)</link>", raw)
    xdates = re.findall(r"<pubDate>([^<>]+?)</pubDate>", raw)
    c = 0
    while c < len(xurls):
        dt = datetime.datetime.strptime(xdates[c].split(' +')[0], "%a, %d %b %Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
        posturl = xurls[c]
        posturl = '%s://%s' % (medios[medio]['portada'].split('://')[0], posturl.split('://')[1])
        posts[posturl] = { 'medio': medio, 'titulo': html.unescape(xtitles[c]), 'fecha': dt }
        c += 1
    return posts

def elterritoriodellince(site=''):
    posts = {}
    raw = getURL(url=sites[site]['feed'])
    rawposts = raw.split('<entry>')[1:]
    for rawpost in rawposts:
        #posttitle = re.findall(r"<title type='text'>([^<>]*?)</title>", raw)[0]
        posttitle = re.findall(r"color: red; font-size: large;&quot;&gt;&lt;b&gt;([^<>]*?)&lt;/b&gt;&lt;/span&gt;", rawpost)[0]
        posturl = re.findall(r"<link rel='alternate' type='text/html' href='([^<>]*?)' title='", rawpost)[0]
        postdate = re.findall(r"<published>(\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d)[^<>]*?</published>", rawpost)[0]
        postimages = re.findall(r"(?i)(https?://[^ ]+?\.(jpg|png))", rawpost)
        postimage = sites[site]['logo']
        if postimages:
            postimage = postimages[0][0]
            for fileurl, fileext in postimages:
                if 's72-c' in fileurl:
                    postimage = fileurl
                    break
        postcontent = re.findall(r"<content type='html'>(.*?)</content>", rawpost)[0]
        postcontent = html.unescape(postcontent)
        postcontent = cleancontent(postcontent)[:250]
        posturl = '%s://%s' % (sites[site]['mainpage'].split('://')[0], posturl.split('://')[1])
        posts[posturl] = { 'site': site, 'title': html.unescape(posttitle), 'date': re.sub('T', ' ', postdate), 'image': postimage, 'content': postcontent }
    return posts

def labocadora(site=''):
    posts = {}
    raw = getURL(url=sites[site]['feed'])
    rawposts = raw.split('<entry>')[1:]
    for rawpost in rawposts:
        posttitle = re.findall(r"<title type='text'>([^<>]*?)</title>", rawpost)[0]
        posturl = re.findall(r"<link rel='alternate' type='text/html' href='([^<>]*?)' title='", rawpost)[0]
        postdate = re.findall(r"<published>(\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d)[^<>]*?</published>", rawpost)[0]
        postimages = re.findall(r"(?i)(https?://[^ ]+?\.(jpg|png))", rawpost)
        postimage = sites[site]['logo']
        if postimages:
            postimage = postimages[0][0]
            for fileurl, fileext in postimages:
                if 's72-c' in fileurl:
                    postimage = fileurl
                    break
        postcontent = re.findall(r"<content type='html'>(.*?)</content>", rawpost)[0]
        postcontent = html.unescape(postcontent)
        postcontent = cleancontent(postcontent)[:250]
        posturl = '%s://%s' % (sites[site]['mainpage'].split('://')[0], posturl.split('://')[1])
        posts[posturl] = { 'site': site, 'title': html.unescape(posttitle), 'date': re.sub('T', ' ', postdate), 'image': postimage, 'content': postcontent }
    return posts

def sputniknews(medio=''):
    posts = {}
    raw = getURL(url=medios[medio]['feed'])
    raw = '<item>'.join(raw.split('<item>')[1:])
    xtitles = re.findall(r"<title>([^<>]*?)</title>", raw)
    xurls = re.findall(r"<link>([^<>]*?)</link>", raw)
    xdates = re.findall(r"<pubDate>([^<>]+?)</pubDate>", raw)
    c = 0
    while c < len(xurls):
        dt = datetime.datetime.strptime(xdates[c].split(' +')[0], "%a, %d %b %Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
        posturl = xurls[c]
        posturl = '%s://%s' % (medios[medio]['portada'].split('://')[0], posturl.split('://')[1])
        posts[posturl] = { 'medio': medio, 'titulo': html.unescape(xtitles[c]), 'fecha': dt }
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
    #posts.append(diariooctubre(medio='diariooctubre'))
    posts.append(elterritoriodellince(site='elterritoriodellince'))
    posts.append(labocadora(site='labocadora'))
    #posts.append(sputniknews(medio='sputniknews'))
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
        postslist.append([props['date'], props['title'], props['image'], props['content'], props['site'], posturl])
    postslist.sort(reverse=True)
    
    c = 0
    output = """<table style="border: 0px;">"""
    for date, title, image, content, site, url in postslist:
        if c % 2 == 0:
           if c != 0:
               output += "\n</tr>" 
           output += "\n<tr>" 
        output += """<td style="border-bottom: 1px solid grey;padding-right: 25px;">
    <p><big>'''[%s %s]'''</big></p>
    <p><a href="%s"><img src="%s" align="right" width="72px" height="72px" /></a>%s[<a href="%s">...</a>]</p>
    <p><small>[%s %s] | %s</small></p>
</td>""" % (url, title, url, image, content, url, sites[site]['mainpage'], sites[site]['name'], date)
        c += 1
    
    output += """</tr>\n</table>"""
    savetable('hemeroteca.wiki', 'ultimasnoticias', output)
            
if __name__ == '__main__':
    main()

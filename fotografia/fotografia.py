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

import csv
import datetime
import random
import re
import time
from xml.etree import ElementTree as ET # para ver los XMl que devuelve flickrapi con ET.dump(resp)

import flickrapi

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
    #load photos in commons
    photodatescommons = []
    with open('../actividad/photos-commons.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            date = row[4]
            photodatescommons.append(date)
    print('Loaded %d metadata' % (len(photodatescommons)))
            
    #sets
    with open('flickr.token', 'r') as f:
        api_key, api_secret = f.read().strip().splitlines()
    
    flickr = flickrapi.FlickrAPI(api_key, api_secret)
    flickruserid = '96396586@N07' #it isn't secret, don't worry
    print('Step 1: authenticate')
    if not flickr.token_valid(perms=u'read'):
        flickr.get_request_token(oauth_callback=u'oob')
        authorize_url = flickr.auth_url(perms=u'read')
        print(authorize_url)
        verifier = unicode(raw_input(u'Verifier code: '), 'utf-8')
        flickr.get_access_token(verifier)
    print('Step 2: use Flickr')
    resp = flickr.photosets.getList(user_id=flickruserid)
    xmlraw = ET.tostring(resp, encoding='utf8', method='xml')
    xmlraw = unicode(xmlraw, 'utf-8')
    photosets = re.findall(ur'(?im) date_create="(\d+)".*?date_update="(\d+)".*?id="(\d+)".*?photos="(\d+)".*?videos="(\d+)"[^<>]*?>\s*<title>([^<>]*?)</title>', xmlraw)
    flickrdone = []
    setrows = []
    c = 1
    for date_create, date_update, photosetid, photos, videos, title in photosets:
        photos = int(photos)
        videos = int(videos)
        date_create = datetime.datetime.fromtimestamp(int(date_create))
        date_update = datetime.datetime.fromtimestamp(int(date_update))
        #how many in commons
        try:
            resp2 = flickr.photosets.getPhotos(photoset_id=photosetid, user_id=flickruserid, extras='date_taken')
        except:
            continue
        xmlraw2 = ET.tostring(resp2, encoding='utf8', method='xml')
        #print(xmlraw2)
        datetakens = re.findall(r'(?im)datetaken="(\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d)"[^<>]*? id="(\d+)"', xmlraw2)
        photosincommons = 0
        photosnotincommons = 0
        for datetaken, photoid in datetakens:
            if datetaken in photodatescommons:
                photosincommons += 1
            else:
                photosnotincommons += 1
        print(photosetid, title, photos, videos, photosincommons, date_create.isoformat(), date_update.isoformat())
        row = u"""
    <tr>
        <td>%s</td>
        <td><a href="https://www.flickr.com/photos/emijrp/albums/%s">%s</a></td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%.1d%%</td>
        <td>%s</td>
        <td>%s</td>
    </tr>""" % (c, photosetid, title, photos, videos, photosincommons, photosincommons/((photosincommons+photosnotincommons)/100.0), date_create.strftime("%Y-%m-%d"), date_update.strftime("%Y-%m-%d"))
        setrows.append(row)
        c += 1
        time.sleep(0.2)
    
    setstable = u"\n<script>sorttable.sort_alpha = function(a,b) { return a[0].localeCompare(b[0], 'es'); }</script>\n"
    setstable += u'\n<table class="wikitable sortable" style="text-align: center;">\n'
    setstable += u"""<tr>
        <th class="sorttable_numeric">#</th>
        <th class="sorttable_alpha">Título</th>
        <th class="sorttable_numeric">Fotos</th>
        <th class="sorttable_numeric">Vídeos</th>
        <th class="sorttable_numeric">En Commons</th>
        <th class="sorttable_numeric">%</th>
        <th class="sorttable_alpha">Creación</th>
        <th class="sorttable_alpha">Actualización</th>
    </tr>"""
    setstable += u''.join(setrows)
    setstable += u'</table>\n'
    savetable('fotografia.wiki', 'tabla sets', setstable)
    
    #tagcloud
    blacklist = [
        'art', 
        'beach', 
        'calles', 
        'de', 
        'la', 
        'museum', 
        'painting', 
        'sea', 
        'spain', 
        'street', 
        'streets', 
    ]
    
    html = ''
    with open('flickrtags.html', 'r') as f:
        html = unicode(f.read(), 'utf-8')
    
    m = re.findall(ur'<a href="/photos/emijrp/tags/([^/]+?)/">([^<>]+?)</a>\s*</td>\s*<td>\s*([^<>]+?)\s*</td>\s*<td class="PhotoCount">\s*<b>(\d+)</b> elementos', html)
    tags = []
    for tag in m:
        tags.append([int(tag[3]), tag[0], tag[2]])
    
    tags.sort(reverse=True)
    c = 0
    cmax = 100
    toptags = []
    for count, tagurl, label in tags:
        skip = False
        for y in label.lower().split(', '):
            if y in [x.lower() for x in blacklist]:
                skip = True
        if skip:
            continue
        c += 1
        bestlabel = ''
        if ', ' in label:
            labels = label.split(', ')
            for label2 in labels:
                if label2 != label2.lower() or \
                    ' ' in label2:
                    bestlabel = label2
        if not bestlabel:
            bestlabel = label.split(', ')[0]
        toptags.append([count, tagurl, bestlabel])
        if c >= cmax:
            break
    
    print(toptags)
    cloud = []
    maxfontsize = 350.0
    minfontsize = 100.0
    maxcount  = toptags[0][0]
    mincount = toptags[-1][0]
    percent = (maxfontsize - minfontsize) / (maxcount - mincount)
    random.shuffle(toptags)
    for count, tagurl, label in toptags:
        size = minfontsize + ((count - mincount) * percent)
        cloud.append(u'<span style="font-size: %s%%;"><a href="https://www.flickr.com/search/?user_id=96396586@N07&sort=date-taken-desc&text=%s&view_all=1">%s</a></span>' % (size, tagurl, label))
    cloud = u' · '.join(cloud)
    savetable('fotografia.wiki', 'nube', cloud)

if __name__ == '__main__':
    main()

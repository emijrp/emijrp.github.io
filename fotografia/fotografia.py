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

import random
import re
import urllib
import urllib.parse

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
    blacklist = [
        'art', 
        'beach', 
        'calles', 
        'de', 
        'museum', 
        'painting', 
        'sea', 
        'street', 
        'streets', 
    ]
    
    html = ''
    with open('flickrtags.html', 'r') as f:
        html = f.read()
    
    m = re.findall(r'<a href="/photos/emijrp/tags/([^/]+?)/">([^<>]+?)</a>\s*</td>\s*<td>\s*([^<>]+?)\s*</td>\s*<td class="PhotoCount">\s*<b>(\d+)</b> elementos', html)
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
    
    cloud = []
    maxfontsize = 350
    minfontsize = 100
    maxcount  = toptags[0][0]
    mincount = toptags[-1][0]
    percent = (maxfontsize - minfontsize) / (maxcount - mincount)
    random.shuffle(toptags)
    for count, tagurl, label in toptags:
        size = minfontsize + ((count - mincount) * percent)
        cloud.append('<span style="font-size: %s%%;"><a href="https://www.flickr.com/search/?user_id=96396586@N07&sort=date-taken-desc&text=%s&view_all=1">%s</a></span>' % (size, tagurl, label))
    cloud = ' · '.join(cloud)
    savetable('fotografia.wiki', 'nube', cloud)

if __name__ == '__main__':
    main()

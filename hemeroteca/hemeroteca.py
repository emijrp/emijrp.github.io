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

import html
import json
import re
import urllib.request

def getURL(url=''):
    req = urllib.request.Request(url=url, data=None, headers={ 'User-Agent': 'Mozilla/5.0' })
    f = urllib.request.urlopen(req)
    return f.read().decode('utf-8')

def elterritoriodellince():
    url = 'https://elterritoriodellince.blogspot.com'
    more = url
    posts = {}
    while more:
        raw = getURL(url=url)
        xtitles = re.findall(r'<span style="color: red; font-size: large;"><b>([^<>]+?)</b></span><br />', raw)
        xposts = re.findall(r"<meta content='(https?://%s[^ ]+?)' itemprop='url'/>" % (url.split('://')[1]), raw)
        xdates = re.findall(r"itemprop='datePublished' title='(\d\d\d\d-\d\d-\d\d)T", raw)
        if len(xposts) != len(xdates):
            print('Error elterritoriodellince')
        else:
            c = 0
            while c < len(xposts):
                posts[xposts[c]] = {'title': html.unescape(xtitles[c]), 'date': xdates[c]}
                c += 1
        more = re.findall(r"<a class='blog-pager-older-link' href='([^ ]+?)' id=", raw)
        more = more and more[0] or ''
        break
    return posts

def main():
    posts = elterritoriodellince()
    print(json.dumps(posts, sort_keys=True))
    with open('hemeroteca.json', 'w') as outfile:
        outfile.write(json.dumps(posts, sort_keys=True))
            
if __name__ == '__main__':
    main()

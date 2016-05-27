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

def main():
    books = []
    userid = "50673985-emilio"
    #https://www.goodreads.com/review/list/50673985-emilio?utf8=✓&utf8=✓&shelf=read&view=table&sort=title&order=a&per_page=100&page=1
    
    #read goodreads profile
    for page in range(1, 10):
        grurl = 'https://www.goodreads.com/review/list/%s?utf8=✓&utf8=✓&shelf=read&view=table&sort=title&order=a&per_page=100&page=%s' % (userid, page)
        print 'Retrieving', grurl
        try:
            req = urllib2.Request(grurl, headers={ 'User-Agent': 'Mozilla/5.0' })
            html = unicode(urllib2.urlopen(req).read(), 'utf-8')
        except:
            break
        
        if not '<td class="field title">' in html:
            break
        
        """
        <td class="field title"><label>title</label><div class="value">    <a title="Vida Inteligente En El Universo" href="/book/show/784249.Vida_Inteligente_En_El_Universo">
      Vida Inteligente En El Universo
</a></div></td>  <td class="field author"><label>author</label><div class="value">      <a href="/author/show/470363.Iosif_Samuilovich_Shklovsky">Shklovsky, Iosif Samuilovich</a>
</div></td>  <td class="field isbn" style="display: none"><label>isbn</label><div class="value">    8429141596
</div></td>  <td class="field isbn13" style="display: none"><label>isbn13</label><div class="value">    9788429141597
</div></td>  <td class="field asin" style="display: none"><label>asin</label><div class="value">
</div></td>  <td class="field num_pages" style="display: none"><label>num pages</label><div class="value">      <nobr>
        0
        <span class="greyText">pp</span>
      </nobr>
</div></td>  <td class="field avg_rating"><label>avg rating</label><div class="value">    4.24
</div></td>  <td class="field num_ratings" style="display: none"><label>num ratings</label><div class="value">    250
</div></td>  <td class="field date_pub" style="display: none"><label>date pub</label><div class="value">      Jan 01, 1966
</div></td>  <td class="field date_pub_edition" style="display: none"><label>date pub edition</label><div class="value">      Apr 02, 1993
</div></td>    
<td class="field rating"><label>my rating</label><div class="value">
        <div class="stars" data-resource-id="784249" data-user-id="50673985" data-submit-url="/review/rate/784249?stars_click=false" data-rating="4"
        """
        #print html
        m = re.finditer(ur'(?im)<td class="field title">\s*<label>\s*title\s*</label>\s*<div class="value">\s*<a title="(?P<title>[^<>]+?)" href="(?P<bookurl>[^<>]+?)">[^<>]*?</a>\s*</div>\s*</td>\s*<td class="field author">\s*<label>\s*author\s*</label>\s*<div class="value">\s*<a href="(?P<authorurl>[^<>]+?)">(?P<author>[^<>]+?)</a>\s*</div>\s*</td>\s*<td class="field isbn" style="display:\s*none">\s*<label>\s*isbn\s*</label>\s*<div class="value">\s*(?P<isbn10>[^<>]+?)\s*</div>\s*</td>\s*<td class="field isbn13" style="display:\s*none">\s*<label>\s*isbn13\s*</label>\s*<div class="value">\s*(?P<isbn13>[^<>]+?)\s*</div>', html)
        for i in m:
            bookprops = {}
            bookprops['title'] = i.group('title').strip()
            bookprops['bookurl'] = i.group('bookurl').strip()
            bookprops['author'] = i.group('author').strip()
            bookprops['authorurl'] = i.group('authorurl').strip()
            bookprops['isbn10'] = i.group('isbn10').strip()
            bookprops['isbn13'] = i.group('isbn13').strip()
            books.append([bookprops['title'], bookprops])
        time.sleep(1)
    books.sort()
    
    bookrows = []
    bookc = 0
    for booktitle, bookprops in books:
        bookc += 1
        customkey = re.sub(ur'(?im)[\"\!\¡\?\¿\#]', '', booktitle)
        row = u"""
    <tr>
        <td>%s</td>
        <td sorttable_customkey="%s"><i><a href="https://www.goodreads.com%s">%s</a></i></td>
        <td><a href="https://www.goodreads.com%s">%s</a></td>
        <td><a href="https://en.wikipedia.org/w/index.php?title=Special:BookSources&isbn=%s">%s</a></td>
        <!--<td>...</td>-->
    </tr>\n""" % (bookc, customkey, bookprops['bookurl'], booktitle, bookprops['authorurl'], bookprops['author'], bookprops['isbn13'], bookprops['isbn13'])
        bookrows.append(row)

    #print table
    table = u"\n<script>sorttable.sort_alpha = function(a,b) { return a[0].localeCompare(b[0], 'es'); }</script>\n"
    table += u'\n<table class="wikitable sortable" style="text-align: center;">\n'
    table += u"""
    <tr>
        <th class="sorttable_numeric">#</th>
        <th class="sorttable_alpha">Título</th>
        <th class="sorttable_alpha">Autoría</th>
        <th class="sorttable_alpha">ISBN</th>
        <!--<th class="sorttable_numeric">Puntos</th>-->
    </tr>"""
    booktable = table
    booktable += u''.join(bookrows)
    booktable += u'</table>\n'
    
    f = open('biblioteca.wiki', 'r')
    html = unicode(f.read(), 'utf-8')
    f.close()
    f = open('biblioteca.wiki', 'w')
    html = u'%s<!-- tabla completa -->%s<!-- /tabla completa -->%s' % (html.split(u'<!-- tabla completa -->')[0], booktable, html.split(u'<!-- /tabla completa -->')[1])
    f.write(html.encode('utf-8'))
    f.close()
    
if __name__ == '__main__':
    main()

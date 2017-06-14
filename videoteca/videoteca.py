#!/usr/bin/env python3
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

"""
ideas:
* guardar los metadatos en un json por si borran algun video y para evitar repedir al servidor lo q ya se sabe (a menos que se fuerce con un parámetro)
* ordenar lista de ids
"""

import os
import subprocess

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
    os.system("python youtube-dl -U")
    
    youtubeids = []
    with open("youtube.ids", "r") as f:
        youtubeids = f.read().strip().splitlines()
    
    youtubevideos = []
    youtubevideosrows = []
    c = 1
    for youtubeid in youtubeids:
        title = subprocess.run(['python', 'youtube-dl', youtubeid, '--get-title'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
        duration = subprocess.run(['python', 'youtube-dl', youtubeid, '--get-duration'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
        print(youtubeid, title, duration)
        youtubevideos.append([youtubeid, title, duration])
        youtubevideosrow = """
    <tr>
        <td>%s</td>
        <td sorttable_customkey="%s"><a href="https://www.youtube.com/watch?v=%s">%s</a></td>
        <td>%s</td>
    </tr>""" % (c, title, youtubeid, title, duration)
        youtubevideosrows.append(youtubevideosrow)
        c += 1
    
    #print table
    youtubevideostable = "\n<script>sorttable.sort_alpha = function(a,b) { return a[0].localeCompare(b[0], 'es'); }</script>\n"
    youtubevideostable += '\n<table class="wikitable sortable" style="text-align: center;">\n'
    youtubevideostable += """
    <tr>
        <th class="sorttable_numeric">#</th>
        <th class="sorttable_alpha">Título</th>
        <th class="sorttable_numeric">Duración</th>
    </tr>"""
    youtubevideostable += ''.join(youtubevideosrows)
    youtubevideostable += '</table>\n'
    #print(youtubevideostable)
    savetable("videoteca.wiki", "youtubevideostable", youtubevideostable)

if __name__ == '__main__':
    main()

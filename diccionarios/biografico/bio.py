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

import os
import re

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
    bios = []
    for filename in os.listdir('.'):
        if filename.endswith('.wiki'):
            f = open(filename, 'r')
            wikicode = unicode(f.read(), 'utf-8')
            f.close()
            headerbio = '{{header-bio' in wikicode and '{{header-bio%s}}' % wikicode.split('{{header-bio')[1].split('}}')[0] or ''
            bioprops = {
                'wiki': re.findall(r"(?im)wiki\s*=([^\n\|]+)", headerbio) and re.findall(r"(?im)wiki\s*=([^\n\|]+)", headerbio)[0] or '', 
                'nombreyapellidos': re.findall(r"(?im)nombre y apellidos\s*=([^\n\|]+)", headerbio) and re.findall(r"(?im)nombre y apellidos\s*=([^\n\|]+)", headerbio)[0] or '', 
                'apellidosynombre': re.findall(r"(?im)apellidos y nombre\s*=([^\n\|]+)", headerbio) and re.findall(r"(?im)apellidos y nombre\s*=([^\n\|]+)", headerbio)[0] or '', 
                'imagen': re.findall(r"(?im)imagen\s*=([^\n\|]+)", headerbio) and re.findall(r"(?im)imagen\s*=([^\n\|]+)", headerbio)[0] or '', 
                'imagentamano': re.findall(r"(?im)imagen tamaño\s*=([^\n\|]+)", headerbio) and re.findall(r"(?im)imagen tamaño\s*=([^\n\|]+)", headerbio)[0] or '', 
                'imagenenlace': re.findall(r"(?im)imagen enlace\s*=([^\n\|]+)", headerbio) and re.findall(r"(?im)imagen enlace\s*=([^\n\|]+)", headerbio)[0] or '', 
                'fechadenacimiento': re.findall(r"(?im)fecha de nacimiento\s*=([^\n\|]+)", headerbio) and re.findall(r"(?im)fecha de nacimiento\s*=([^\n\|]+)", headerbio)[0] or '', 
                'lugardenacimiento': re.findall(r"(?im)lugar de nacimiento\s*=([^\n\|]+)", headerbio) and re.findall(r"(?im)lugar de nacimiento\s*=([^\n\|]+)", headerbio)[0] or '', 
                'fechadefallecimiento': re.findall(r"(?im)fecha de fallecimiento\s*=([^\n\|]+)", headerbio) and re.findall(r"(?im)fecha de fallecimiento\s*=([^\n\|]+)", headerbio)[0] or '', 
                'lugardefallecimiento': re.findall(r"(?im)lugar de fallecimiento\s*=([^\n\|]+)", headerbio) and re.findall(r"(?im)lugar de fallecimiento\s*=([^\n\|]+)", headerbio)[0] or '', 
                'descripcion': re.findall(r"(?im)descripcion\s*=([^\n\|]+)", headerbio) and re.findall(r"(?im)descripcion\s*=([^\n\|]+)", headerbio)[0] or '', 
            }
            for k, v in [['fechadenacimiento', 'anyodenacimiento'], ['fechadefallecimiento', 'anyodefallecimiento']]:
                if bioprops[k]:
                    t = bioprops[k].split()[-1].strip()
                    t = len(t) == 4 and str(int(t)) == t and str(t) or '-'
                    bioprops[v] = t
                else:
                    bioprops[v] = '-'
            if bioprops['lugardenacimiento']:
                bioprops['pais'] = bioprops['lugardenacimiento'].split(', ')[-1]
            if bioprops['wiki']:
                bios.append([bioprops['wiki'], bioprops])
    bios.sort()
    print(len(bios),'bios')
    
    biorows = []
    bioc = 1
    for biowiki, bioprops in bios:
        biorow = u"""
    <tr>
        <td>%s</td>
        <td sorttable_customkey="%s"><a href="%s.html">%s</a></td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
    </tr>\n""" % (bioc, bioprops['apellidosynombre'], bioprops['wiki'], bioprops['apellidosynombre'], bioprops['pais'], bioprops['anyodenacimiento'], bioprops['anyodefallecimiento'], bioprops['descripcion'])
        biorows.append(biorow)
        bioc += 1
    
    #print table
    biotable = u"\n<script>sorttable.sort_alpha = function(a,b) { return a[0].localeCompare(b[0], 'es'); }</script>\n"
    biotable += u'\n<table class="wikitable sortable" style="text-align: center;">\n'
    biotable += u"""
    <tr>
        <th class="sorttable_numeric">#</th>
        <th class="sorttable_alpha">Nombre</th>
        <th class="sorttable_alpha">País</th>
        <th class="sorttable_alpha">Nacimiento</th>
        <th class="sorttable_alpha">Fallecimiento</th>
        <th class="sorttable_alpha">Descripción</th>
    </tr>"""
    biotable += u''.join(biorows)
    biotable += u'</table>\n'
    
    biogallery = u""
    for biowiki, bioprops in bios:
        biogallery += '<a href="%s.html"><img src="../../images/%s" width="80px" height="100px" title="%s" /></a>' % (bioprops['wiki'], bioprops['imagen'], bioprops['nombreyapellidos'])
    
    savetable('index.wiki', u'tabla completa', biotable)
    savetable('index.wiki', u'galería completa', biogallery)

if __name__ == '__main__':
    main()

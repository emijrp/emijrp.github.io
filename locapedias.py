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
import urllib

def main():
    locapedias = {
        'Almeriapedia': {
            'api': 'https://almeriapedia.wikanda.es/w/api.php', 
            'dump': 'https://archive.org/details/wiki-almeriapediawikandaes_w', 
            'country': 'España', 
            'region': 'Provincia de Almería', 
        }, 
        'Arija': {
            'api': 'http://www.arija.org/es/api.php', 
            'dump': 'https://archive.org/details/wiki-arijaorg_es', 
            'country': 'España', 
            'region': 'Arija', 
        }, 
        'Ateneo de Córdoba': {
            'api': 'http://www.ateneodecordoba.com/api.php', 
            'dump': 'https://archive.org/details/wiki-ateneodecordobacom', 
            'country': 'España', 
            'region': 'Córdoba', 
        }, 
        'Comuni-Italiani.it': {
            'api': 'http://rete.comuni-italiani.it/w/api.php', 
            'dump': 'https://archive.org/details/wiki-retecomuni_italianiit_w', 
            'country': 'Italia', 
            'region': '', 
        }, 
        'Cádizpedia': {
            'api': 'https://cadizpedia.wikanda.es/w/api.php', 
            'dump': 'https://archive.org/details/wiki-cadizpediawikandaes_w', 
            'country': 'España', 
            'region': 'Provincia de Cádiz', 
        }, 
        'Córdobapedia': {
            'api': 'https://cordobapedia.wikanda.es/w/api.php', 
            'dump': 'https://archive.org/details/wiki-cordobapediawikandaes_w', 
            'country': 'España', 
            'region': 'Provincia de Córdoba', 
        }, 
        'CTpedia': {
            'api': 'http://www.ctpedia.es/w/api.php', 
            'dump': 'https://archive.org/details/wiki-ctpediaes_w', 
            'country': 'España', 
            'region': 'Cartagena', 
        }, 
        'DeLebrija': {
            'api': 'http://www.delebrija.es/index.php/Portada', 
            'dump': '', 
            'country': 'España', 
            'region': 'Lebrija', 
            'status': 'offline', 
        }, 
        'Enciclopedia Guanche': {
            'api': 'http://www.guanches.org/enciclopedia/api.php', 
            'dump': 'https://archive.org/details/wiki-guanchesorg_enciclopedia', 
            'country': 'España', 
            'region': 'Islas Canarias', 
        }, 
        'Enciclopedia de Oviedo': {
            'api': 'http://el.tesorodeoviedo.es', 
            'dump': '', 
            'country': 'España', 
            'region': 'Oviedo', 
        }, 
        'EnnstalWiki': {
            'api': 'http://ennstalwiki.at/w/api.php', 
            'dump': '', 
            'country': 'Austria', 
            'region': 'Enns river valey', 
        }, 
        'EnWada': {
            'api': 'http://enwada.es/w/api.php', 
            'dump': 'https://archive.org/details/wiki-enwadaes_w', 
            'country': 'España', 
            'region': 'Provincia de Guadalajara', 
        }, 
        'Granadapedia': {
            'api': 'https://granadapedia.wikanda.es/w/api.php', 
            'dump': 'https://archive.org/details/wiki-granadapediawikandaes_w', 
            'country': 'España', 
            'region': 'Provincia de Granada', 
        }, 
        'Huelvapedia': {
            'api': 'https://huelvapedia.wikanda.es/w/api.php', 
            'dump': 'https://archive.org/details/wiki-huelvapediawikandaes_w', 
            'country': 'España', 
            'region': 'Provincia de Huelva', 
        }, 
        'Jaenpedia': {
            'api': 'https://jaenpedia.wikanda.es/w/api.php', 
            'dump': 'https://archive.org/details/wiki-jaenpediawikandaes_w', 
            'country': 'España', 
            'region': 'Provincia de Jaén', 
        }, 
        'JerezSiempre': {
            'api': 'http://www.jerezsiempre.com/api.php', 
            'dump': 'https://archive.org/details/wiki-jerezsiemprecom', 
            'country': 'España', 
            'region': 'Jerez de la Frontera', 
        }, 
        'LeonWiki': {
            'api': 'http://leonwiki.lazorrera.com', 
            'dump': '', 
            'country': 'España', 
            'region': 'León', 
            'status': 'offline', 
        }, 
        'LinaWiki': {
            'api': 'http://leonwiki.lazorrera.com', 
            'dump': 'https://archive.org/details/enciclopediadelinarescom_wiki-20110427-wikidump.7z', 
            'country': 'España', 
            'region': 'Linares', 
            'status': 'offline', 
        }, 
        'Madripedia': {
            'api': 'http://www.madripedia.es', 
            'dump': 'https://archive.org/details/wiki-madripediaes_w', 
            'country': 'España', 
            'mirror': 'https://madripedia.wikis.cc', 
            'region': 'Comunidad de Madrid', 
            'status': 'offline', 
        }, 
        'Málaga Diwiki': {
            'api': 'http://malaga.diwiki.org', 
            'dump': '', 
            'country': 'España', 
            'region': 'Málaga', 
            'status': 'offline', 
        }, 
        'Málagapedia': {
            'api': 'http://malagapedia.wikanda.es/w/api.php', 
            'dump': 'https://archive.org/details/wiki-malagapediawikandaes_w', 
            'country': 'España', 
            'region': 'Provincia de Málaga', 
        }, 
        'Malawi360': {
            'api': 'http://www.malawi360.com', 
            'dump': 'https://archive.org/details/wiki-malawi360com_wiki', 
            'country': 'Malawi', 
            'founded': '2007-08-24', 
            'region': 'Malawi', 
        }, 
        'MiToledo': {
            'api': 'http://wiki.mitoledo.com', 
            'dump': '', 
            'country': 'España', 
            'region': 'Toledo', 
            'status': 'offline', 
        }, 
        'PlanetNepal': {
            'api': 'http://planetnepal.org/w/api.php', 
            'dump': '', 
            'country': 'Nepal', 
            'founded': '2010-01-31', 
            'region': 'Nepal', 
        }, 
        'Rosèspedia': {
            'api': 'http://rosespedia.cat/w/api.php', 
            'dump': '', 
            'country': 'España', 
            'region': 'Roses', 
        }, 
        'Sevillapedia': {
            'api': 'https://sevillapedia.wikanda.es/w/api.php', 
            'dump': 'https://archive.org/details/wiki-sevillapediawikandaes_w', 
            'country': 'España', 
            'region': 'Provincia de Sevilla', 
        }, 
        'Stadtwiki Karlsruhe': {
            'api': 'https://sevillapedia.wikanda.es/w/api.php', 
            'dump': '', 
            'country': 'Alemania', 
            'founded': '2004-07-22', 
            'region': 'Karlsruhe', 
        }, 
        'Tarracowiki': {
            'api': 'http://www.tarracowiki.cat/w/api.php', 
            'dump': 'https://archive.org/details/wiki-tarracowikicat_tarracowiki', 
            'country': 'España', 
            'founded': '', 
            'region': 'Tarragona', 
        }, 
        'Tomsk Wiki': {
            'api': 'http://towiki.ru/w/api.php', 
            'dump': '', 
            'country': 'Rusia', 
            'founded': '2007-01-29', 
            'region': 'Tomsk', 
        }, 
        'UgandaWiki': {
            'api': 'http://www.ugandawiki.ug', 
            'dump': '', 
            'country': 'Uganda', 
            'founded': '', 
            'region': 'Uganda', 
            'status': 'offline', 
        }, 
        'Vilapedia': {
            'api': 'http://www.vila-real.info/vilapedia2015/', 
            'dump': 'https://archive.org/details/vila_realinfo_vilapedia-20110427-wikidump.7z', 
            'country': 'España', 
            'founded': '', 
            'mirror': 'https://vilapedia.wikis.cc', 
            'region': 'Villareal', 
            'status': 'offline', 
        }, 
        'Wikanda': {
            'api': 'http://www.vila-real.info/vilapedia2015/', 
            'dump': 'https://archive.org/details/wiki-wikandaes_w', 
            'country': 'España', 
            'founded': '', 
            'region': 'Andalucía', 
        }, 
        'WikiBurgos': {
            'api': 'http://www.wikiburgos.es/w/api.php', 
            'dump': 'https://archive.org/details/wiki-wikiburgoses', 
            'country': 'España', 
            'founded': '', 
            'region': 'Burgos', 
        }, 
        'WikiExtremadura': {
            'api': 'http://www.wikiextremadura.org', 
            'dump': '', 
            'country': 'España', 
            'founded': '', 
            'region': 'Extremadura', 
            'status': 'offline', 
        }, 
        'WikiLleida': {
            'api': 'http://www.wikilleida.cat', 
            'dump': '', 
            'country': 'España', 
            'founded': '', 
            'region': 'Lleida', 
            'status': 'offline', 
        }, 
        'WikiMurcia': {
            'api': 'http://wikimurcia.com', 
            'dump': '', 
            'country': 'España', 
            'founded': '', 
            'region': 'Murcia', 
        }, 
        'WikiPakistan': {
            'api': 'http://pakistan.wikia.com', 
            'dump': '', 
            'country': 'Pakistán', 
            'founded': '', 
            'region': 'Pakistán', 
        }, 
        'WikiRioja': {
            'api': 'http://wikirioja.com', 
            'dump': 'https://archive.org/details/wiki-wikiriojacom', 
            'country': 'España', 
            'founded': '', 
            'region': 'La Rioja', 
        }, 
        'WikiSalamanca': {
            'api': 'http://www.wikisalamanca.org', 
            'dump': 'https://archive.org/details/wiki-wikisalamancaorg', 
            'country': 'España', 
            'founded': '', 
            'mirror': 'https://wikisalamanca.wikis.cc', 
            'region': 'Provincia de Salamanca', 
            'status': 'offline', 
        }, 
        'WikiTunisie': {
            'api': 'http://www.wikitunisie.org', 
            'dump': '', 
            'country': 'Túnez', 
            'founded': '', 
            'region': 'Túnez', 
            'status': 'offline', 
        }, 
        'Xilocapedia': {
            'api': 'http://www.xiloca.com/xilocapedia/api.php', 
            'dump': 'https://archive.org/details/wiki-xilocacom_xilocapedia', 
            'country': 'España', 
            'founded': '', 
            'region': 'Valle del Jiloca', 
        }, 
        'Zaragoza Diwiki': {
            'api': 'http://zaragoza.diwiki.org', 
            'dump': '', 
            'country': 'España', 
            'founded': '', 
            'region': 'Zaragoza', 
            'status': 'offline', 
        }, 
    }
    locapedias2 = locapedias.copy()
    
    for locapedia, locaprops in locapedias.items():
        locapedias2[locapedia]['name'] = locapedia
        if 'status' in locaprops and locaprops['status'].lower() == 'offline':
            continue
        
        siteinfourl = '%s?action=query&meta=siteinfo&siprop=general|statistics&format=json' % (locaprops['api'])
        siteinfo = {}
        try:
            req = urllib.Request(siteinfourl, headers={ 'User-Agent': 'Mozilla/5.0' })
            html = unicode(urllib.urlopen(req).read(), 'utf-8')
            siteinfo = json.loads(html)
            locapedias2[locapedia]['status'] = 'online'
        except:
            locapedias2[locapedia]['status'] = 'offline'
            pass
        
        if 'query' in siteinfo and 'general' in siteinfo['query']:
            for prop in ['base', 'generator', 'lang', 'logo']:
                locapedias2[locapedia][prop] = prop in siteinfo['query']['general'] and siteinfo['query']['general'][prop] or ''
        else:
            print('Error while retrieving siteinfo for %s %s' % (locapedia, siteinfourl))
        
        if 'query' in siteinfo and 'statistics' in siteinfo['query']:
            for prop in ['articles', 'edits', 'images', 'pages']:
                locapedias2[locapedia][prop] = prop in siteinfo['query']['statistics'] and siteinfo['query']['statistics'][prop] or ''
        else:
            print('Error while retrieving statistics for %s %s' % (locapedia, siteinfourl))
    
    locapedias3 = [[v['name'].lower(), v] for k, v in locapedias2.items()]
    locapedias3.sort()
    locarows = []
    locac = 1
    for locapedia, locaprops in locapedias3:
        if locaprops['status'].lower() == 'offline':
            locaprops['status'] = 'Offline'
        elif locaprops['status'].lower() == 'online':
            locaprops['status'] = 'Online'
        locarow = u"""
    <tr>
        <td>%s</td>
        <td><a href="%s">%s</a></td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td><a href="https://web.archive.org/web/*/%s">IA</a></td>
    </tr>\n""" % (locac, 'base' in locaprops and locaprops['base'] or '', locaprops['name'], 'founded' in locaprops and locaprops['founded'] or '', locaprops['region'], locaprops['country'], 'articles' in locaprops and locaprops['articles'] or '?', 'pages' in locaprops and locaprops['pages'] or '?', 'images' in locaprops and locaprops['images'] or '?', 'users' in locaprops and locaprops['users'] or '?', locaprops['status'], 'dump' in locaprops and locaprops['dump'] and '<a href="%s">Dump</a>' % (locaprops['dump']) or '', 'mirror' in locaprops and locaprops['mirror'] and '<a href="%s">Mirror</a>' % (locaprops['mirror']) or '', 'base' in locaprops and locaprops['base'] or '')
        locarows.append(locarow)
        locac += 1
    
    #print table
    table = "\n<script>sorttable.sort_alpha = function(a,b) { return a[0].localeCompare(b[0], 'es'); }</script>\n"
    table += '\n<table class="wikitable sortable" style="text-align: center;">\n'
    table += """
    <tr>
        <th class="sorttable_numeric">#</th>
        <th class="sorttable_alpha">Locapedia</th>
        <th class="sorttable_alpha">Fundación</th>
        <th class="sorttable_alpha">Región</th>
        <th class="sorttable_alpha">País</th>
        <th class="sorttable_numeric">Artículos</th>
        <th class="sorttable_numeric">Páginas</th>
        <th class="sorttable_numeric">Imágenes</th>
        <th class="sorttable_numeric">Usuarios</th>
        <th class="sorttable_alpha">Estado</th>
        <th class="sorttable_alpha">Dump</th>
        <th class="sorttable_alpha">Mirror</th>
        <th class="sorttable_alpha">IA</th>
    </tr>"""
    locatable = table
    locatable += ''.join(locarows)
    locatable += '</table>\n'
    
    with open('locapedias.wiki', 'r') as f:
        html = f.read()
    with open('locapedias.wiki', 'w') as g:
        html = '%s<!-- tabla completa -->%s<!-- /tabla completa -->%s' % (html.split(u'<!-- tabla completa -->')[0], locatable, html.split('<!-- /tabla completa -->')[1])
        g.write(html)
        
if __name__ == '__main__':
    main()

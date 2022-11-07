#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2017-2022 emijrp <emijrp@gmail.com>
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
import json
import re
import sys

def main():
    #load json files
    foto = {}
    with open('actividad-foto.json', 'r') as infile:
        foto = json.loads(infile.read())
    
    software = {}
    with open('actividad-software.json', 'r') as infile:
        software = json.loads(infile.read())
    
    wiki = {}
    with open('actividad-wiki.json', 'r') as infile:
        wiki = json.loads(infile.read())
    
    #sum subtotals
    total = {}
    for subtotal in [foto, wiki, software]:
        for k, v in subtotal.items():
            if k in total:
                total[k] += v
            else:
                total[k] = v
    
    #save json total
    with open('actividad-total.json', 'w') as outfile:
        outfile.write(json.dumps(total, indent=4, sort_keys=True))
    print('Saved in actividad-total.json')

if __name__ == '__main__':
    main()

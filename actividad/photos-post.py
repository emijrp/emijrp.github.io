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

"""
ideas:
* mirar cuantas fotos he subido a commons y a flickr por año y ver cuales podria subir a commons que sean utiles

"""

def main():
    for filename, datepos in [
        ['photos-commons.csv', 4], 
        ['photos-flickr.csv', 2],
        ]:
        print(filename)
        years = {}
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                date = row[datepos]
                year = date.split('-')[0]
                if year in years:
                    years[year] += 1
                else:
                    years[year] = 1
        years_list = [[year, count] for year, count in years.items()]
        years_list.sort()
        print('\n'.join(['%s: %s' % (year, count) for year, count in years_list]))

if __name__ == '__main__':
    main()

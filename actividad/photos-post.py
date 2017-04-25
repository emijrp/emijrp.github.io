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
    years = {}
    with open('photos.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            date = row[4]
            year = date.split(':')[0]
            if year in years:
                years[year] += 1
            else:
                years[year] = 1
    print(years)

if __name__ == '__main__':
    main()

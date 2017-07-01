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

import datetime
import getpass
import json
import re
import sys
import time
import urllib2

from github import Github

def main():
    userregexp = re.compile(r'(?im)emijrp')
    activity = {}
    
    #github (pip install pygithub)
    print("Introduce user and password for GitHub")
    username = raw_input("Username: ")
    password = getpass.getpass('Password: ')
    g = Github(username, password)
    for repo in g.get_user().get_repos():
        print(repo.full_name, repo.fork)
        if not repo.fork: #saltar los fork que puede tener miles de commits y solo apenas 1 o 2 mios de algun pull-request
            if re.search(r'(?im)toollabs', repo.full_name):
                continue
            for commit in repo.get_commits():
                #commit.author es mejor que commit.committer
                #el committer a veces es web-flow (via web?)
                #el commit.author a veces no existe si el autor no existe en github
                #por eso controlo en el if que no sea None
                if commit.author != None and re.search(userregexp, commit.author.login):
                    unixtime = commit.commit.author.date.strftime('%s')
                    if activity.has_key(unixtime):
                        activity[unixtime] += 1
                    else:
                        activity[unixtime] = 1
        time.sleep(1)
    
    #googlecode
    #not needed, exported to github
    
    #rediris
    #defunct
    
    #save json
    with open('actividad-software.json', 'w') as outfile:
        outfile.write(json.dumps(activity, indent=4, sort_keys=True))

if __name__ == '__main__':
    main()

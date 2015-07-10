# -*- coding: utf-8 -*-

'''
    Genesis Add-on
    Copyright (C) 2015 lambda

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import re
import client


def unpack(script):
    aSplit = script.split(";',")
    p = str(aSplit[0])
    aSplit = aSplit[1].split(",")
    a = int(aSplit[0])
    c = int(aSplit[1])
    k = aSplit[2].split(".")[0].replace("'", '').split('|')
    e = ''
    d = ''

    sUnpacked = str(__unpack(p, a, c, k, e, d))
    sUnpacked = sUnpacked.replace('\\', '')

    url = __parse(sUnpacked)
    return url


def __unpack(p, a, c, k, e, d):
    while (c > 1):
        c = c -1
        if (k[c]):
            p = re.sub('\\b' + str(__itoa(c, a)) +'\\b', k[c], p)
    return p


def __itoa(num, radix):
    result = ""
    while num > 0:
        result = "0123456789abcdefghijklmnopqrstuvwxyz"[num % radix] + result
        num /= radix
    return result


def __parse(sUnpacked):
    url = re.compile("'file' *, *'(.+?)'").findall(sUnpacked)
    url += re.compile("file *: *[\'|\"](.+?)[\'|\"]").findall(sUnpacked)
    url += re.compile("playlist=(.+?)&").findall(sUnpacked)
    url += client.parseDOM(sUnpacked, "embed", ret="src")

    url = [i for i in url if not i.endswith('.srt')]

    url = 'http://' + url[-1].split('://', 1)[-1]
    return url


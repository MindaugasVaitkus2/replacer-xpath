#!/usr/bin/env python

import sys, os, re, requests, fnmatch, os.path

from pprint import pprint
from urlparse import urljoin

from lxml import html, etree

"""
Accepts the following tuple, path to files, filetype, xpath to content you would like to replace, replacement content.
Create a list of files to operate on.
Consume list with def 
"""

includes = ['*.htm', '*.html']

# Translate the filename match into a regular expression.
# includes becomes '.*\\.htm\\Z(?ms)|.*\\.html\\Z(?ms)'
includes = r'|'.join([fnmatch.translate(x) for x in includes])

pathbase = '/home/oliver/temp'

"""
This block is a for loop which uses the regular expression named includes
to filter for results. The file is then joined back to it's underlying path.
Finally the full filename is appended to a list named "filestoedit".
"""
for root, dirs, files in os.walk(pathbase, topdown=True):
    for f in files:
        if re.match(includes, f):
            fullpath = os.path.join(root, f)
            filestoedit.append(fullpath)

for f in filestoedit:
    print f
    parser = etree.HTMLParser() # elementtree etree
    tree = etree.parse("f", parser)
# Find the script element containing the old google ad code.
# More specific, will only match what we seek.
    tree010.xpath('.//script[contains(., "google_ad_format")]')
# Find the script element linking to the js for displaying the old ad
# More specific, will only match what we seek.
    tree010.xpath('.//script[@src="http://pagead2.googlesyndication.com/pagead/show_ads.js"]')

# Assign the advert branches to named variables so we can manipulate them.
    googad01 = tree010.xpath('.//script[contains(., "google_ad_format")]')[0]
    googad02 = tree010.xpath('.//script[contains(., "google_ad_format")]')[1]

googjs01 = tree010.xpath('.//script[@src="http://pagead2.googlesyndication.com/pagead/show_ads.js"]')[0]
googjs02 = tree010.xpath('.//script[@src="http://pagead2.googlesyndication.com/pagead/show_ads.js"]')[1]


""" To consume an invalid XML or HTML file which contains fragments of
 interest we will use Python's file reading capabilities to create a
 string object. This string object will then be serialised into an html
 fragment by lxml using lxml.html.fragments_fromstring function.
"""
adfragment = open("adsense-ad.file", "r")
adfrag = adfragment.read()
adfragment.close()

# Each part of the former string will be found at a list address.
# newad[0], newad[3], etc
newad = html.fragments_fromstring(adfrag)

ad_para01 = googad01.getparent()
ad_para02 = googad02.getparent()

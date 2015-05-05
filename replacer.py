#!/usr/bin/env python

import sys, os, re, argparse, os.path

import requests, fnmatch

from pprint import pprint
from urlparse import urljoin

from lxml import html, etree

"""
Accepts the following positional arguments, pathname, xpath(s) to content you would like to replace, path(s) to replacement content. Create a list of files to check for replacement(s). Consume list with sleuth().
"""

parser = argparse.ArgumentParser(description='Find and replace content in XML/HTML files using xpath')
parser.add_argument('pathname', help='Directory containing files you would like to change')
parser.add_argument('ekspath', help='Xpath expression to find target content')
parser.add_argument('content', help='Content that will replace target')

args = parser.parse_args()

# This could be changed in the future by accepting an argument that sets
# which etree parser we will be using.
includes = ['*.htm', '*.html']

# Translate the filename match into a regular expression.
# includes becomes '.*\\.htm\\Z(?ms)|.*\\.html\\Z(?ms)'
includes = r'|'.join([fnmatch.translate(x) for x in includes])

pathname = '/home/oliver/temp'

filestoedit = []

"""
This block is a for loop which uses the regular expression named includes to filter for results. The file is then joined back to it's underlying path.  Finally the full filename is appended to the list named "filestoedit".
"""
def sleuth(pathname):
    if os.path.exists(pathname): #Check that the directory exists.
        for root, dirs, files in os.walk(pathname, topdown=True):
            for f in files:
                if re.match(includes, f): #Apply regex named includes.
                    fullpath = os.path.join(root, f)
                    filestoedit.append(fullpath)
    else:
        print "The directory {} does not exist, please check your entry.".format(pathname)

for f in filestoedit:
    print f
    parser = etree.HTMLParser() # elementtree etree
# Find the script element containing the old google ad code.
# More specific, will only match what we seek.
    tree = etree.parse(f, parser)
    tree.xpath('.//script[contains(., "google_ad_format")]')
# Find the script element linking to the js for displaying the old ad
# More specific, will only match what we seek.
    tree.xpath('.//script[@src="http://pagead2.googlesyndication.com/pagead/show_ads.js"]')

# Assign the advert branches to named variables so we can manipulate them.
    googad01 = tree.xpath('.//script[contains(., "google_ad_format")]')[0]
    googad02 = tree.xpath('.//script[contains(., "google_ad_format")]')[1]

    googjs01 = tree.xpath('.//script[@src="http://pagead2.googlesyndication.com/pagead/show_ads.js"]')[0]
    googjs02 = tree.xpath('.//script[@src="http://pagead2.googlesyndication.com/pagead/show_ads.js"]')[1]

"""
To consume an invalid XML or HTML file which contains fragments of interest we will use Python's file reading capabilities to create a string object. This string object will then be serialised into an html fragment by lxml using lxml.html.fragments_fromstring function.
"""
adfragment = open("adsense-ad.file", "r")
adfrag = adfragment.read()
adfragment.close()

# Each part of the former string will be found at a list address.
# newad[0], newad[3], etc
newad = html.fragments_fromstring(adfrag)

ad_para01 = googad01.getparent()
ad_para02 = googad02.getparent()

if __name__ == '__main__':
    sleuth()


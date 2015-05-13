#!/usr/bin/env python

import sys
import os
import re
import argparse
import requests
import fnmatch

from pprint import pprint
from urlparse import urljoin
from lxml import html, etree

"""
Accepts the following positional arguments, pathname, xpath(s) to
content you would like to replace, path(s) to replacement content.
Create a list of files to check for replacement(s). Consume list
with sleuth().
"""


def get_args():
    '''This function parses and returns arguments passed in'''
    parser = argparse.ArgumentParser(
        description='Find and replace content in XML/HTML files using xpath.')
    parser.add_argument('-f', '--filetype', type=str, default='html',
        choices=('xml', 'html', 'htm'))
    parser.add_argument('-p', '--pathname', type=str, default='./',
        help='Starting path of files to change. Default is current directory.')
    parser.add_argument('-c', '--content', type=str, required=True,
        help='Content that will replace target. Path to file or xpath')
    parser.add_argument('-x', '--xpath', type=str, nargs='+', required=True,
        help='Xpath expression(s) to find target content.')
    # Array for all arguments passed to script
    args = parser.parse_args()
    # Assign args to variables
    pathname = args.pathname
    content = args.content
    ekspath = args.xpath
    filetype = args.filetype
    return pathname, ekspath, content, filetype

# Match return values from main() and assign to their respective variables
pathname, ekspath, content, filetype = get_args()

print pathname
print content
#if len(ekspath) > 1:
#    for eks in ekspath:
#        print eks
#else:
print ekspath
print filetype

''' Set includes for filetype filtering via re.match below.
Choose parser based on filetype argument.'''
if 'htm' in (filetype):
    includes = ['*.htm', '*.html']
    parser = etree.HTMLParser()
else:
    filetype == 'xml'
    includes = ['*.xml']
    parser = etree.XMLParser()

print parser

"""Translate the filename match into a regular expression.
includes becomes '.*\\.htm\\Z(?ms)|.*\\.html\\Z(?ms)'"""
includes = r'|'.join([fnmatch.translate(x) for x in includes])

filestoedit = []

# can this be setup to operate on a single file?
""" Loop that only finds files of specified filetype. The filename including
the path is appended to the list named "filestoedit".
"""
def main(pathname):
    if os.path.exists(pathname): #Check that the directory exists.
        for root, dirs, files in os.walk(pathname, topdown=True):
            for f in files:
                if re.match(includes, f): #Apply regex named includes.
                    fullpath = os.path.join(root, f)
                    filestoedit.append(fullpath)
#uncomment me       gobble()
    else:
        print
        "The directory {} does not exist, please check \
        your entry.".format(pathname)

"""
os.access(pathtofile, os.R_OK) may not be necessary
"""
"""
The xpath goes here to match the content we want to replace.
We should perform some type of sanity check on the input.
Set up exception handling, failover for non-matches.
We need to return the number of matches so we can target
them via list manipulation.
Use the lxml "open in browser" feature to display the first
matching changed page and provide the option to abort."""

# To create a tree run main(pathname) if you haven't yet to populate the list
# filestoedit[]. Then choose a file from the list, say filestoedit[5]. If you
# want to find a specific path via name with a matching list index you can
# run this block:
# substring = 'search_for_me'
# for index, string in enumerate(list_of_files):
#     if substring in string:
#         print index, string
# Now you can open a file:
# filevar = open(filestoedit[13])
# then you can run the tree parser line from below, and work with the tree

def gobble(filestoedit):
    for pathtofile in filestoedit:
        try:
            with open(pathtofile) as f:
                tree = etree.parse(f, parser)
                for path in ekspath:
                        print path
# how to perform the replace? should i test for container elements such as
# <p> <div> etc? if None then place new content in div before the old content
# once the element is returned from the xpath it may be interacted with via
# the etree module, thus we could check for container elements with
# .getparent()
        except IOError as e:
            print("%s reading %s." % e, pathtofile)
# Raise exception..?

# The following block is being generalized above.
# Assign the advert branches to named variables so we can manipulate them.
#    googad01 = tree.xpath('.//script[contains(., "google_ad_format")]')[0]
#    googad02 = tree.xpath('.//script[contains(., "google_ad_format")]')[1]
#    googjs01 = tree.xpath('.//script[@src="http://pagead2.googlesyndication.com/pagead/show_ads.js"]')[0]
#    googjs02 = tree.xpath('.//script[@src="http://pagead2.googlesyndication.com/pagead/show_ads.js"]')[1]

"""To consume an invalid XML or HTML file which contains fragments of interest
we will use Python's file reading capabilities to create a string object. This
string object will then be serialised into an html fragment by lxml using
lxml.html.fragments_fromstring function."""
def file_fragment(content):
    fragment = open(content, "r")
    fraglines = fragment.readlines() # creates a list of lines
# join the lines and strip extra whitespace
    fragsmush = "".join(line.rstrip() for line in fraglines)
# parse the fragment into elements at elemfrag[:]
# for el in elemfrag; print html.tostring(el)
    elemfrag = html.fragments_fromstring(fragsmush)
    fragment.close()
# Each part of the former string will be found at a list address.
# newad[0], newad[3], etc
    newad = html.fragments_fromstring(adfrag)
    ad_para01 = googad01.getparent()
    ad_para02 = googad02.getparent()


if __name__ == '__main__':
    get_args()

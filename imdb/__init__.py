### BEGIN LICENSE
# -*- coding: utf-8 -*-

#    Copyright (c) 2011 David Calle <rcarvalhoxavier@gmail.com>

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

import logging
import optparse
import urllib2
import json
import re

import gettext
from gettext import gettext as _
gettext.textdomain('imdb')

from singlet.lens import SingleScopeLens, IconViewCategory, ListViewCategory

from imdb import imdbconfig

class ImdbLens(SingleScopeLens):

    class Meta:
        name = 'imdb'
        description = 'Imdb Lens'
        search_hint = 'Search Imdb'
        icon = 'IMDb_logo.svg'
        search_on_blank=False
	categories = ['Popular Movies','Exact Movies']

    # TODO: Add your categories
    imdbSearchUrl = "http://www.imdb.com/xml/find?json=1&nr=1&tt=on&q="
    imdbUrl = "http://www.imdb.com/title/"
    imdbDetails = "http://app.imdb.com/title/"
    imdbCategoryPopular = ListViewCategory("Titulos Populares", "dialog-information-symbolic")
    imdbCategoryExact = IconViewCategory("Titulos Exatos", "dialog-information-symbolic")
    imdbCategorySubstring = IconViewCategory("Titulos contidos", "dialog-information-symbolic")


    def searchMovies(self,kindTitle,jsonResult,results):
	try:
		result = jsonResult[kindTitle]
		for r in result:
			url = ("%s%s/maindetails" % (self.imdbDetails,r['id']))
			jsonResult = json.loads(urllib2.urlopen(url).read())
			imdbDetails = jsonResult['data']
	
			if kindTitle == 'title_popular':
				category = self.imdbCategoryPopular
			elif kindTitle == 'title_exact':
				category = self.imdbCategoryExact
			elif kindTitle == 'title_substring':
				category = self.imdbCategorySubstring
			try:
				image = imdbDetails['image']
				image = image['url']
			except KeyError, e:
				image =  '/usr/share/unity/lenses/imdb/unity-lens-imdb.svg'
			print "%s - %s - %s" % (r['id'],r['title'],imdbDetails['rating'])
	
			link = "%s%s" % (self.imdbUrl,r['id'])
			
			title = re.sub(r"<a href='/name\/[nmtt][nmtt]\d{7}/'>|</a>","",r['description'])
	
			results.append(link,
                         image,
                         category,
                         "text/html",
                         "%s - %s" % (r['title'],imdbDetails['rating']),
                         title,
                         link)
	except KeyError, e:
		return results
	return results


    def search(self, search, results):
	if len(search) > 0 and len(search) < 3:
		return

	print "Searching %s" % (search)
        # TODO: Add your search results
	search = search.replace(" ", "|")
	url = ("%s%s" % (self.imdbSearchUrl,search))

	jsonResult = json.loads(urllib2.urlopen(url).read())
	print 'jsonResult %s '% len(jsonResult)

	if len(jsonResult) == 0:
		return

	self.searchMovies('title_popular',jsonResult,results)
	self.searchMovies('title_exact',jsonResult,results)
#	self.searchMovies('title_substring',jsonResult,results)
	results
        pass

from local import *

import json
from tornado import ioloop,web

import pymongo
from bson import json_util
from bson.objectid import ObjectId

# Mongo setting
connection = pymongo.MongoClient(MONGODB_SERVER, MONGODB_PORT)
db = connection.sg_grocery
items = db.table


class ItemHandler(web.RequestHandler):

    def get(self, item_id):

		print 'loading item id = ' + item_id
		product = items.find_one({
			'_id': ObjectId(item_id)
		})
		self.render("item.html", 
					page_title="Item: " + product['title'] + " - CraiGrocery", 
					product=product)


class SearchHandler(web.RequestHandler):

    def get(self):

		keyword = self.get_argument("keyword", "", True)
		sortBy = self.get_argument("sort", "", True)
		order = self.get_argument("order", "", True)

		# check length of keyword
		if len(keyword.replace(" ", "")) < 3:
			self.render("index.html", title="Redo your search, please! ")
		else:
			keyword = keyword.lower()

		# validate sortBy (default = "key")
		if sortBy != "now_price" and sortBy != "merchant":
			sortBy = "key"

		# validate order (default = "1")
		if order != "-1":
			order = "1"

		print ('loading search result = ' + keyword + ' sortby ' + sortBy + 
				" in order of " + order)

		# search in Mongo
		products = (items.find({ 
						'key': { '$regex' :".*" + keyword + ".*"}
						}).sort(
							[(sortBy, int(order))]
						)
					)

		self.render("search.html", 
					page_title="'" + keyword + "' search result - CraiGrocery", 
					products=products)

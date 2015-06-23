from local import *

import json
from tornado import ioloop,web

import pymongo
from bson import json_util
from bson.objectid import ObjectId


class ItemHandler(web.RequestHandler):

    def get(self, item_id):

		print 'loading item id = ' + item_id

		connection = pymongo.MongoClient(MONGODB_SERVER, 27017)
		db = connection.sg_grocery
		items = db.table

		product = items.find_one({
			'_id': ObjectId(item_id)
		})

		self.render("item.html", title="The item detail", product=product)

		# self.set_header("Content-Type", "application/json")
		# self.write(json.dumps((products),default=json_util.default))


class SearchHandler(web.RequestHandler):

    def get(self):

		keyword = self.get_argument("keyword", None, True)
		sortBy = self.get_argument("sort", "", True)
		print 'loading search result = ' + keyword + ' sortby ' + sortBy

		if len(keyword) < 3:
			self.render("index.html", title="Redo your search, please! ")
		else:
			keyword = keyword.lower()

		connection = pymongo.MongoClient(MONGODB_SERVER, 27017)
		db = connection.sg_grocery
		items = db.table

		if sortBy == 'price':
			products = items.find({ 'key': { '$regex' :".*" + keyword + ".*"} }).sort([("now_price", 1), ])
		elif sortBy == 'merchant':
			products = items.find({ 'key': { '$regex' :".*" + keyword + ".*"} }).sort([("merchant", 1), ])
		else:
			products = items.find({ 'key': { '$regex' :".*" + keyword + ".*"} }).sort([("key", 1), ])

		self.render("search.html", title="Your search result", products=products)

from local import *

import json
from tornado import ioloop,web

import pymongo
from bson import json_util
from bson.objectid import ObjectId


class ItemHandler(web.RequestHandler):

    def get(self, item_id):

		print 'finding item id = ' + item_id

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

		user_input = self.get_argument("user_input", None, True)
		if len(user_input) < 3:
			self.render("index.html", title="Redo your search, please! ")
		else:
			user_input = user_input.lower()

		connection = pymongo.MongoClient(MONGODB_SERVER, 27017)
		db = connection.sg_grocery
		items = db.table

		products = items.find({ 'key': { '$regex' :".*" + user_input + ".*"} })

		self.render("search.html", title="Your search result", products=products)

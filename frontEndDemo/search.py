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

		stories = items.find_one({
			'_id': ObjectId(item_id)
		})
		self.set_header("Content-Type", "application/json")
		self.write(json.dumps((stories),default=json_util.default))


class SearchHandler(web.RequestHandler):

    def get(self):

		user_input = self.get_argument("user_input", None, True)
		if len(user_input) < 3:
			self.render("index.html")

		connection = pymongo.MongoClient(MONGODB_SERVER, 27017)
		db = connection.sg_grocery
		items = db.table

		stories = items.find({ 'key': { '$regex' :".*" + user_input + ".*"} })

		self.render("search.html", title="Your search result", stories=stories)

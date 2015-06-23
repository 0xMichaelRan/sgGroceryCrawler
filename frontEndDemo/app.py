import os
from tornado import ioloop,web
from pymongo import MongoClient
import json

from search import SearchHandler
from search import ItemHandler

class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("index.html", title="My title")


class BaseHandler(web.RequestHandler):
    def get(self):
        students = []
        students.append('student')
        students.append('student2')
        students.append('student3')

        self.render("base.html", students=students)

class BoldHandler(web.RequestHandler):
    def get(self):
        students = []
        students.append('student')
        students.append('student2')
        students.append('student3')

        self.render("bold.html", students=students)



settings = {
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "debug" : True
}
 
application = web.Application([
    (r'/', IndexHandler),
    (r'/index', IndexHandler),
    (r'/item/(.+)', ItemHandler),
    (r'/search', SearchHandler),
    (r'/base', BaseHandler),
    (r'/bold', BoldHandler),
],**settings)
 
if __name__ == "__main__":
    print 'Running (listen on port 8888)'
    application.listen(8888)
    ioloop.IOLoop.instance().start()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os.path
import cyclone.web
from twisted.python import log
from twisted.internet import reactor
import urllib
from TSUtils import *
from NBUtils import *


class SearchHandler(cyclone.web.RequestHandler):
    def do_search(self):
        term = self.get_argument("term", None)
        page = self.get_argument("page", None)
        if (term == None):
            self.write('you need to set a term to search')
            return
        ts = TSUtils()
        search_results = ts.search(term, page)
        self.render("tweet.html", tweets=search_results, term=term, next_page=str(int(page)+1))

    def post(self):
        self.do_search()

    def get(self):
        self.do_search()
            
class ClassifyHandler(cyclone.web.RequestHandler):
    def post(self):
        for a in range(0,50):
            tweet = self.get_argument("tweet["+str(a)+"]", None)
            type = self.get_argument("ctype["+str(a)+"]", None)
            if (tweet != None):
                tweet_file_classification(tweet,type)
        print "term.... ", self.get_argument("cterm", "None")
        self.redirect("/search?page=" + self.get_argument("next_page") + '&term=' + urllib.quote(self.get_argument("cterm", "")))


class ViewHandler(cyclone.web.RequestHandler):
    def do_search_and_classify(self):
        term = self.get_argument("term", None)
        page = self.get_argument("page", 1)
        if (term == None):
            self.write('you need to set a term to search')
            return

        ts = TSUtils()
        search_results = ts.search(term, page)
        classi = classify(search_results)
        self.render("tweet_view.html", tweets=search_results, classi=classi, term=term, page=str(int(page)+1))

    def get(self):
        self.do_search_and_classify()

    def post(self):
        self.do_search_and_classify()



def main():
    settings = {
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "xheaders": True,
        }
    
    handlers = [
        (r"/", cyclone.web.RedirectHandler, {"url": "/static/index.html"}),
        (r"/search", SearchHandler),
        (r"/classify", ClassifyHandler),
        (r"/view", ViewHandler),
        ]
    
    application = cyclone.web.Application(handlers, **settings)
    reactor.listenTCP(8888, application)
    reactor.run()

if __name__ == "__main__":
    log.startLogging(sys.stdout)
    main()

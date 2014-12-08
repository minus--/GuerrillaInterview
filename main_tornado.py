__author__ = 'Amine Kerkeni'

import tornado.ioloop
import tornado.web
import tornado.httpserver
import json
import requests
from sqlalchemy import create_engine,Table, MetaData, Column, Index, String, Integer, Text


engine = create_engine('mysql://my_user:my_password@127.0.0.1/coding_interview')


class IndexHandler(tornado.web.RequestHandler):
    """
    Standard web handler that returns the index page
    """
    def get(self,assignment_id):
        try:
            assignment = engine.execute('SELECT title, details FROM coding_assignment WHERE id = %s' % assignment_id).fetchone()
            self.render("index.html", title=assignment.title, details=assignment.details, assignment_id= assignment_id)
        except Exception as ex:
            print ex


class DefaultSampleHandler(tornado.web.RequestHandler):
    """
    Standard web handler that returns the index page
    """
    def get(self,assignment_id, language_id):
        try:
            sample = engine.execute('SELECT initial_code FROM coding_assignment_default \
                                     WHERE coding_assignment_id = %s AND language = %s'
                                    % (assignment_id, language_id)).fetchone()
            self.set_header("Content-Type", "application/json")
            self.write(json.dumps({'sample': sample.initial_code}))
        except Exception as ex:
            print ex

class RextesterHandler(tornado.web.RequestHandler):
    """
    This handler will relay post messages to rextester API in order to avoid cross domain issues.
    Rextester API is an online service for compiling/running code
    """
    def post(self):
        data = json.loads(self.request.body)
        code = data['Program']
        language = data['LanguageChoiceWrapper']
        headers = {'content-type': 'application/json'}
        payload = {u'LanguageChoiceWrapper': int(language), u'Program': code}
        r = requests.post("http://rextester.com/rundotnet/api", data=json.dumps(payload), headers=headers)
        self.set_header("Content-Type", "application/json")
        self.write(r.json())

class Application(tornado.web.Application):
    """
    Main application class
    """
    def __init__(self):
        handlers = [
            (r'/([0-9]+)', IndexHandler),
            (r'/sample/([0-9]+)/([0-9]+)', DefaultSampleHandler),
            (r'/run', RextesterHandler),
            ]
        settings = {
            "template_path": 'templates',
            "static_path": 'static',
            }
        tornado.web.Application.__init__(self, handlers, debug=True, **settings)


if __name__ == '__main__':
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(5000)
    tornado.ioloop.IOLoop.instance().start()
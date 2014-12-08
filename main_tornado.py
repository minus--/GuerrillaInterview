__author__ = 'Amine Kerkeni'

import tornado.ioloop
import tornado.web
import tornado.httpserver
import json
import requests
from sqlalchemy import create_engine,Table, MetaData, Column, Index, String, Integer, Text
import hashlib
import base64
import uuid


engine = create_engine('mysql://my_user:my_password@127.0.0.1/coding_interview')


salt = 'whrfbpUjQuibLL5SdFzE2w=='


def check_permission(password, username):
    user_details = engine.execute("SELECT email, password FROM users WHERE email = '%s'" % username).fetchone()
    if user_details is not None:
        t_sha = hashlib.sha512()
        t_sha.update(password+salt)
        hashed_password = base64.urlsafe_b64encode(t_sha.digest())
        if hashed_password == user_details.password:
            return True
        else:
            False
    return False


class LoginHandler(tornado.web.RequestHandler):
    """
    User login handler
    """
    def get(self):
        try:
            error_message = self.get_argument("error")
        except:
            error_message = ""
        self.render("login.html", error_message=error_message)

    def post(self):
        username = self.get_argument("email", "")
        password = self.get_argument("password", "")
        auth = check_permission(password, username)
        if auth:
            self.set_current_user(username)
            self.redirect(self.get_argument("next", u"/1"))
        else:
            error_msg = u"?error=" + tornado.escape.url_escape("Login incorrect")
            self.redirect(u"/login/" + error_msg)

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie("user", tornado.escape.json_encode(user))
        else:
            self.clear_cookie("user")


class IndexHandler(tornado.web.RequestHandler):
    """
    Standard web handler that returns the index page
    """
    def get(self,assignment_id=1):
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
            (r'/login', LoginHandler),
            (r'/sample/([0-9]+)/([0-9]+)', DefaultSampleHandler),
            (r'/run', RextesterHandler),
            ]

        settings = {
            "template_path": 'templates',
            "static_path": 'static',
            "cookie_secret": "MY COOKIE SECRET FOR TEST",
            "login_url": "/login"
            }
        tornado.web.Application.__init__(self, handlers, debug=True, **settings)


if __name__ == '__main__':
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(5000)
    tornado.ioloop.IOLoop.instance().start()
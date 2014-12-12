__author__ = 'Amine Kerkeni'

import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.web import url
import json
import requests
from sqlalchemy import create_engine,Table, MetaData, Column, Index, String, Integer, Text
import hashlib
import base64
import uuid
import config
import time

engine = create_engine(config.sql_connection_string)


def check_permission(password, username):
    user_details = engine.execute("SELECT email, password, salt FROM users WHERE email = '%s'" % username).fetchone()
    if user_details is not None:
        t_sha = hashlib.sha512()
        t_sha.update(password+user_details.salt)
        hashed_password = base64.urlsafe_b64encode(t_sha.digest())
        if hashed_password == user_details.password:
            return True
        else:
            False
    return False


def check_token_validity(token, timeout):
    if token is None:
        return True
    else:
        if (time.time() - float(token)) > float(timeout):
            return False
        else:
            return True


class BaseHandler(tornado.web.RequestHandler):
        def get_current_user(self):
            return self.get_secure_cookie("user")


class LoginHandler(BaseHandler):
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
            self.redirect(self.get_argument("next", u"/list"))
        else:
            error_msg = u"?error=" + tornado.escape.url_escape("Login incorrect")
            self.redirect(u"/login")

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie("user", tornado.escape.json_encode(user))
        else:
            self.clear_cookie("user")


class AssignmentListHandler(BaseHandler):
    """
    Standard web handler that returns the index page
    """
    @tornado.web.authenticated
    def get(self,assignment_id=1):
        assignments = engine.execute('SELECT id, title, level FROM coding_assignment LIMIT 0,10').fetchall()

        self.render("list.html",assignment_list=assignments)


class AssignmentHandler(BaseHandler):
    """
    Standard web handler that returns the index page
    """
    @tornado.web.authenticated
    def get(self,assignment_id=1):
        user = self.get_secure_cookie("user")
        user = user.replace('@', '_').replace('"', '')
        token_id = '%s_assignment_%s' % (user, assignment_id)
        token = self.get_secure_cookie(token_id)
        if check_token_validity(token, 30):
            if token is None:
                self.set_secure_cookie(token_id, str(time.time()))
            try:
                assignment = engine.execute('SELECT title, details FROM coding_assignment WHERE id = %s'
                                            % assignment_id).fetchone()

                self.render("assignment.html", title=assignment.title, details=assignment.details,
                            assignment_id=assignment_id)
            except Exception as ex:
                print ex
        else:
            self.render("login.html")

    @tornado.web.authenticated
    def post(self,assignment_id=1):
        user = self.get_secure_cookie("user")
        user = user.replace('@', '_').replace('"', '')
        token_id = '%s_assignment_%s' % (user, assignment_id)
        timer = self.get_secure_cookie(token_id)
        if timer is not None:
            user_code = self.get_argument("code_area", "")
            print user_code
            if (time.time() - float(timer)) > 30:
                self.clear_cookie(token_id)
                self.redirect("/login")
            else:
                self.clear_cookie(token_id)
                self.redirect("/list")
        else:
            self.redirect("/login")


class ExpiredAssignmentHandler(BaseHandler):
    """
    Standard web handler that returns the index page
    """
    @tornado.web.authenticated
    def get(self,assignment_id=1):
        pass


class DefaultSampleHandler(BaseHandler):
    """
    Standard web handler that returns the index page
    """
    @tornado.web.authenticated
    def get(self,assignment_id, language_id):
        try:
            sample = engine.execute('SELECT initial_code FROM coding_assignment_default \
                                     WHERE coding_assignment_id = %s AND language = %s'
                                    % (assignment_id, language_id)).fetchone()
            self.set_header("Content-Type", "application/json")
            self.write(json.dumps({'sample': sample.initial_code}))
        except Exception as ex:
            print ex


class RextesterHandler(BaseHandler):
    """
    This handler will relay post messages to rextester API in order to avoid cross domain issues.
    Rextester API is an online service for compiling/running code
    """
    @tornado.web.authenticated
    def post(self):
        data = json.loads(self.request.body)
        code = data['Program']
        language = data['LanguageChoiceWrapper']
        headers = {'content-type': 'application/json'}
        payload = {u'LanguageChoiceWrapper': int(language), u'Program': code}
        r = requests.post("http://rextester.com/rundotnet/api", data=json.dumps(payload), headers=headers)
        self.set_header("Content-Type", "application/json")
        self.write(r.json())


class LogoutHandler(BaseHandler):
    """
    User logout handler
    """
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/login"))


class Application(tornado.web.Application):
    """
    Main application class
    """
    def __init__(self):
        handlers = [
            url(r'/assignment/([0-9]+)', AssignmentHandler, name='assignment'),
            url(r'/list', AssignmentListHandler, name='list'),
            url(r'/login', LoginHandler, name='login'),
            url(r'/logout', LogoutHandler, name="logout"),
            (r'/sample/([0-9]+)/([0-9]+)', DefaultSampleHandler),
            (r'/run', RextesterHandler),
            ]

        settings = {
            "template_path": 'templates',
            "static_path": 'static',
            "cookie_secret": config.cookie_secret,
            "login_url": "/login"
            }
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(5000)
    tornado.ioloop.IOLoop.instance().start()
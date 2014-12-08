__author__ = 'Amine'

import requests
import json
import pickle
import hashlib
import base64
import uuid
import config
from sqlalchemy import create_engine,Table, MetaData, Column, Index, String, Integer, Text

engine = create_engine(config.sql_connection_string)

def rextester_run():
    headers = {'content-type': 'application/json'}
    data = {u'LanguageChoiceWrapper': 5, u'Program': u'print "Hello Amine"'}
    r = requests.post("http://rextester.com/rundotnet/api", data=json.dumps(data), headers=headers)
    print r
    print r.status_code
    print r.encoding
    print r.text
    print r.json()


salt = base64.urlsafe_b64encode(uuid.uuid4().bytes)
print salt

def hash_password(msg):
    password = msg
    t_sha = hashlib.sha512()
    t_sha.update(password+salt)
    hashed_password =  base64.urlsafe_b64encode(t_sha.digest())
    return hashed_password


def validate_password(msg, hash):
    t_sha = hashlib.sha512()
    t_sha.update(msg+salt)
    hashed_password =  base64.urlsafe_b64encode(t_sha.digest())
    if hashed_password == hash:
        return True
    else:
        return False


def save_password(email, password, user_salt):
    try:
        hashed_password = hash_password(password)
        engine.execute("INSERT INTO users (email,password,salt) VALUES ('%s' , '%s', '%s')"
                       % (email, hashed_password, user_salt))
    except Exception as ex:
        print ex

print validate_password('toto',hash_password('toto'))
print validate_password('tito',hash_password('toto'))

save_password('toto.toto@gmail.com','toto', salt)
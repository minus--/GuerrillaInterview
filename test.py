__author__ = 'Amine'

import requests
import json
import pickle

headers = {'content-type': 'application/json'}
data = {u'LanguageChoiceWrapper': 5, u'Program': u'print "Hello Amine"'}
r = requests.post("http://rextester.com/rundotnet/api", data=json.dumps(data), headers=headers)
print r
print r.status_code
print r.encoding
print r.text
print r.json()


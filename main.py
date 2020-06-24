import requests
import json
import base64

from truyenfulldb import TruyenFullDatabase
from models import Categories, Chapters, Books

import logging

user = 'test'
pythonapp = 'hKO0 ZLsb LxAJ MnRe QgqR IZCI'
url = "http://test.com/wp-json/wp/v2"
data_string = user + ':' + pythonapp
token = base64.b64encode(data_string.encode())
headers = {'Authorization': 'Basic ' + token.decode('utf-8')}

db = TruyenFullDatabase(dbname=r'truyenfull.db')

for book in db.session.query(Books).all()[0:1]:
    # print(book.name)
    # print(book.category, type(book.category))
    # break
    post = {'title': book.name,
            'status': 'publish',
            'content': book.description,
            'tac-gia': '7,8,9,10',
            'categories': '1,2,3'
            }
    print(post)
    r = requests.post(url + '/posts', headers=headers, json=post)
    print(json.loads(r.content.decode('utf-8')))
    #print('Your post is published on ' + json.loads(r.content.decode('utf-8'))['link'])

# data_string = user + ':' + pythonapp
# data_bytes = data_string.encode("utf-8")

post = {'title': 'First rest api chapter1',
        'status': 'publish',
        'content': 'this is the content post',
        'author': '2',
        'parent':'32',
        'slug':'truyen-5-first-rest-api-chapter1'
        }

r = requests.post(url + '/chapters', headers=headers, json=post)
# print('Your post is published on ' + json.loads(r.content)['link'])
print('Your post is published on ' + json.loads(r.content.decode('utf-8'))['link'])
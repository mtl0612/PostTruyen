import base64
import requests
import json
from functools import lru_cache
import ring
import pprint

import logging

pp = pprint.PrettyPrinter(indent=4,depth=2)

## for test server local
# pythonapp = 'EAuw ICsv 0vSy XcVL xSxQ uurH'
# url = "http://test-v.com/wp-json/wp/v2"

# ## for webdoctruyen.net
user = 'webdoctruyenposter'
pythonapp = 'LfZa jh8n 8jGI WS6M kolj T6ow'
url = "https://webdoctruyen.net/wp-json/wp/v2"

## for webdoctruyen.net
# pythonapp = 'u462 ACBr GPt0 gnsE w9Hi XSOk'
# url = "http://test.webdoctruyen.net/wp-json/wp/v2"


data_string = user + ':' + pythonapp
token = base64.b64encode(data_string.encode())
headers = {'authorization': 'Basic ' + token.decode('utf-8'),
           'content_type': r'application\/json'}
print(headers)

@ring.lru()
def get_book(slug):
    book_url = url + f'/posts?slug={slug}'
    r = requests.get(book_url, headers=headers)
    logging.info(f"Download from {book_url}")
    try:
       return json.loads(r.content.decode('utf-8'))[0]
    except:
        return None
    #print(json.loads(r.content.decode('utf-8')))

@ring.lru()
def get_author(slug):
    author_url = url + f'/tac-gia?slug={slug}'
    r = requests.get(author_url, headers=headers)
    logging.info(f"Download from {author_url}")
    #print(json.loads(r.content.decode('utf-8')))
    try:
        return json.loads(r.content.decode('utf-8'))[0]
    except:
        return None


@ring.lru()
def get_category(slug):
    category_url = url + f'/categories?slug={slug}'
    r = requests.get(category_url , headers=headers)
    logging.info(f"Download from {category_url }")
    try:
        return json.loads(r.content.decode('utf-8'))[0]
    except:
        return None


@ring.lru()
def get_chapter(slug):
    chapter_url = url + f'/chapters?slug={slug}'
    r = requests.get(chapter_url , headers=headers)
    logging.info(f"Download from {chapter_url }")
    try:
        return json.loads(r.content.decode('utf-8'))[0]
    except:
        return None

@ring.lru()
def get_image(slug):
    image_url = url + f'/media?slug={slug}'
    r = requests.get(image_url , headers=headers)
    logging.info(f"Download from {image_url }")
    try:
        return json.loads(r.content.decode('utf-8'))[0]
    except:
        return None

def post_book(book_dict):
    post_book_url = url + '/posts'
    r = requests.post(post_book_url, headers = headers, json = book_dict)
    get_book.delete(book_dict['slug'])
    return json.loads(r.content.decode('utf-8'))

def post_image(image_dict):
    post_image_url = url + '/media'
    r = requests.post(post_image_url, headers = headers, files = image_dict)
    get_image.delete(image_dict['slug'])
    return json.loads(r.content.decode('utf-8'))

def post_chapter(chapter_dict):
    post_chapter_url = url + '/chapters'
    r = requests.post(post_chapter_url, headers = headers, json = chapter_dict)
    get_chapter.delete(chapter_dict['slug'])
    return json.loads(r.content.decode('utf-8'))

def post_author(author_dict):
    post_author_url = url + '/tac-gia'
    r = requests.post(post_author_url, headers = headers, json = author_dict)
    get_author.delete(author_dict['slug'])
    logging.debug(r)
    return json.loads(r.content.decode('utf-8'))

def post_category(category_dict):
    post_category_url = url + '/categories'
    r = requests.post(post_category_url, headers = headers, json = category_dict)
    logging.debug(r.content.decode('utf-8'))
    get_category.delete(category_dict['slug'])
    return json.loads(r.content.decode('utf-8'))

if __name__ == "__main__":
    pp.pprint(get_book("test-post-truyen"))
    pp.pprint(get_book("anh-se-yeu-em-nhung-ngay-troi-tro-gio"))
    pp.pprint(get_book("chet-sap-bay-roi"))
    print(get_book("chet-sap-bay-roi"))
    print(get_author("nguyen-nhat-anh"))
    print(get_author("nguyen-nhat-anh"))
    print(get_author("a"))
    print(get_author("a"))
    print(get_category("kiem-hiep"))
    print(get_category("kiem-hiep"))
    print(get_chapter("test-post-truyen-chuong-1"))

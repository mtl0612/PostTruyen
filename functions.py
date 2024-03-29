import base64
import requests
import json
from functools import lru_cache
import ring
import pprint

import logging

pp = pprint.PrettyPrinter(indent=4,depth=2)

## for test server local
# user = 'test'
# pythonapp = 'EAuw ICsv 0vSy XcVL xSxQ uurH'
# url = "http://test.com/wp-json/wp/v2"

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
# print(headers)

@ring.lru()
def get_book(slug):
    book_url = url + f'/posts?slug={slug}'
    logging.info(f"Download from {book_url}")
    r = requests.get(book_url, headers=headers)
    try:
       return json.loads(r.content.decode('utf-8'))[0]
    except IndexError:
        return None
    #print(json.loads(r.content.decode('utf-8')))

@ring.lru()
def get_author(slug):
    author_url = url + f'/tac-gia?slug={slug}'
    logging.info(f"Download from {author_url}")
    r = requests.get(author_url, headers=headers)
    #print(json.loads(r.content.decode('utf-8')))
    try:
        return json.loads(r.content.decode('utf-8'))[0]
    except IndexError:
        return None


@ring.lru()
def get_category(slug):
    category_url = url + f'/categories?slug={slug}'
    logging.info(f"Download from {category_url}")
    r = requests.get(category_url , headers=headers)
    try:
        return json.loads(r.content.decode('utf-8'))[0]
    except IndexError:
        return None


@ring.lru()
def get_chapter(slug):
    chapter_url = url + f'/chapters?slug={slug}'
    logging.info(f"Download from {chapter_url }")
    r = requests.get(chapter_url , headers=headers)
    try:
        return json.loads(r.content.decode('utf-8'))[0]
    except IndexError:
        return None

@ring.lru()
def get_image(slug):
    image_url = url + f'/media?slug={slug}'
    logging.info(f"Download from {image_url }")
    r = requests.get(image_url , headers=headers)
    try:
        return json.loads(r.content.decode('utf-8'))[0]
    except IndexError:
        return None

def post_book(book_dict):
    post_book_url = url + '/posts'
    logging.info(f"Post to {post_book_url} slug: {book_dict['slug']}")
    r = requests.post(post_book_url, headers = headers, json = book_dict)
    get_book.delete(book_dict['slug'])
    return json.loads(r.content.decode('utf-8'))

def post_image(image_dict):
    post_image_url = url + '/media'
    logging.info(f"Post to {post_image_url} slug: {image_dict['slug']}")
    r = requests.post(post_image_url, headers = headers, files = image_dict)
    get_image.delete(image_dict['slug'])
    return json.loads(r.content.decode('utf-8'))

def post_chapter(chapter_dict):
    post_chapter_url = url + '/chapters'
    logging.info(f"Posting to {post_chapter_url} slug: {chapter_dict['slug']}....")
    r = requests.post(post_chapter_url, headers = headers, json = chapter_dict)
    r_json = json.loads(r.content.decode('utf-8'))
    logging.info(f"Posted to {r_json['link']}")
    get_chapter.delete(chapter_dict['slug'])
    return r_json

def post_author(author_dict):
    post_author_url = url + '/tac-gia'
    logging.info(f"Post to {post_author_url} slug: {author_dict['slug']}")
    r = requests.post(post_author_url, headers = headers, json = author_dict)
    get_author.delete(author_dict['slug'])
    logging.debug(r)
    return json.loads(r.content.decode('utf-8'))

def post_category(category_dict):
    post_category_url = url + '/categories'
    logging.info(f"Post to {post_category_url} slug: {book_dict['slug']}")
    r = requests.post(post_category_url, headers = headers, json = category_dict)
    logging.debug(r.content.decode('utf-8'))
    get_category.delete(category_dict['slug'])
    return json.loads(r.content.decode('utf-8'))

def update_chapter(chapter_id, chapter_dict):
    update_chapter_url = url + '/chapters/' + str(chapter_id)
    logging.info(f"Post to {update_chapter_url} slug: {chapter_dict['slug']}")
    r = requests.post(update_chapter_url, headers = headers, json = chapter_dict)
    get_chapter.delete(chapter_dict['slug'])
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

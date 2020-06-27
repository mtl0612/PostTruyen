import base64
import requests
import json
from functools import lru_cache
import ring
import pprint

pp = pprint.PrettyPrinter(indent=4,depth=2)

user = 'test'
pythonapp = 'hKO0 ZLsb LxAJ MnRe QgqR IZCI'
url = "http://test.com/wp-json/wp/v2"
data_string = user + ':' + pythonapp
token = base64.b64encode(data_string.encode())
headers = {'Authorization': 'Basic ' + token.decode('utf-8')}

@ring.lru()
def get_book(slug):
    book_url = url + f'/posts?slug={slug}'
    r = requests.get(book_url, headers=headers)
    print(f"Download from {book_url}")
    try:
       return json.loads(r.content.decode('utf-8'))[0]
    except:
        return None
    #print(json.loads(r.content.decode('utf-8')))

@ring.lru()
def get_author(slug):
    author_url = url + f'/tac-gia?slug={slug}'
    r = requests.get(author_url, headers=headers)
    print(f"Download from {author_url}")
    #print(json.loads(r.content.decode('utf-8')))
    try:
        return json.loads(r.content.decode('utf-8'))[0]
    except:
        return None


@ring.lru()
def get_category(slug):
    category_url = url + f'/categories?slug={slug}'
    r = requests.get(category_url , headers=headers)
    print(f"Download from {category_url }")
    try:
        return json.loads(r.content.decode('utf-8'))[0]
    except:
        return None


@ring.lru()
def get_chapter(slug):
    chapter_url = url + f'/chapters?slug={slug}'
    r = requests.get(chapter_url , headers=headers)
    print(f"Download from {chapter_url }")
    try:
        return json.loads(r.content.decode('utf-8'))[0]
    except:
        return None


def post_book(book_json):
    post_book_url = url + '/posts'
    r = requests.post(post_book_url, headers = headers, json = book_json)
    return json.loads(r.content.decode('utf-8'))

def post_author(author_json):
    post_author_url = url + '/tac-gia'
    r = requests.post(post_author_url, headers = headers, json = author_json)
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

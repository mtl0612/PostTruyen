import pprint
import logging
from time import sleep
from operator import attrgetter

from truyenfulldb import TruyenFullDatabase
from models import Categories, Chapters, Books
from functions import get_chapter, get_category, get_book, get_author
from functions import post_book, post_author, post_category, post_chapter

from slugify import slugify
from  natsort import natsorted

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

pp = pprint.PrettyPrinter(indent=4,depth=2)

db = TruyenFullDatabase(dbname=r'D:\01_PycharmProjects\GetTruyen\gettruyen\database\truyenfull.db')

slugattrgetter = attrgetter('slug')
for book in db.session.query(Books).all():
    print("book.slug", book.slug)
    print("book.author", book.author)
    print("book.category", book.category)

    slug = book.slug
    book_json = get_book(slug)
    if book_json is None:
        author_ids = []
        if book.author is not None:
            authors = [x.strip() for x in book.author.split(",")]
            for author in authors:
                try:
                    author_id = get_author(slugify(author))['id']
                except TypeError:
                    author_dict = {'name' : author, 'slug' : slugify(author)}
                    author_id = post_author(author_dict)['id']
                author_ids.append(author_id)

        category_ids = []
        for category in book.category:
            try:
                category_id = get_category(category.slug)['id']
            except TypeError:
                category_dict = {'name' : category.name, 'slug' : category.slug}
                print("category_dict", category_dict)
                category_id = post_category(category_dict)['id']
            category_ids.append(category_id)

        print("author_ids", author_ids)
        print("category_ids", category_ids)
        if book.status == "Đang ra":
            book_status = "Đang cập nhật"
        else:
            book_status = "Hoàn thành"
        book_dict = {'title': book.name,
                'status': 'publish',
                'slug' : book.slug,
                'content': book.description,
                'tac-gia': ','.join([str(x) for x in author_ids]),
                'categories' : ','.join([str(x) for x in category_ids]),
                'tw_multi_chap' : '1',
                'tw_status' : book_status
                }
        #pp.pprint(book_dict)
        book_json = post_book(book_dict)
    #pp.pprint(natsorted([x.url for x in book.chapter]))
    chapters = [x for x in book.chapter]
    for chapter in natsorted(chapters, key = slugattrgetter):
        chapter_slug = '-'.join([book.slug, chapter.slug])
        chapter_json = get_chapter(chapter_slug)
        if chapter_json is None:
            chapter_dict = {'title': chapter.name,
                    'status': 'publish',
                    'slug' : chapter_slug,
                    'content' : chapter.content,
                    'parent' : book_json['id']
                    }
            # pp.pprint(chapter_dict)
            post_chapter(chapter_dict)
            # print(chapter)
            sleep(1)


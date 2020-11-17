import os
import pprint
import logging
import concurrent

import configparser

from time import sleep
from operator import attrgetter
from sqlalchemy import asc

from models import Categories, Chapters, Books

from truyenfulldb import TruyenFullDatabase
from functions import get_chapter, get_category, get_book, get_author, get_image
from functions import post_book, post_author, post_category, post_chapter, post_image
from functions import update_chapter
from logging import getLogger, getLevelName, Formatter, StreamHandler

from concurrent.futures import ThreadPoolExecutor
from slugify import slugify
from natsort import natsorted

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


log = getLogger()
log.setLevel(getLevelName('INFO'))
log_formatter = Formatter("%(asctime)s [%(levelname)s] %(name)s: [%(threadName)s] %(message)s" , "%m-%d %H:%M:%S" )
if (log.hasHandlers()):
    log.handlers.clear()
console_handler = StreamHandler()
console_handler.setFormatter(log_formatter)
file_handle = logging.FileHandler('run.log')
file_handle.setLevel(logging.INFO)
file_handle.setFormatter(log_formatter)
log.addHandler(console_handler)
log.addHandler(file_handle)

pp = pprint.PrettyPrinter(indent=4,depth=2)

slugattrgetter = attrgetter('slug')
media_path = r"C:\PycharmProject\PostTruyen\images"

def worker(offset, limit, workerid):
    db = TruyenFullDatabase(dbname=r'truyenfull.db')
    log.info(f'worker id {workerid} started!')
    start_id = offset
    end_id = offset + limit

    config = configparser.ConfigParser()
    config_file_name = 'thread_'+str(workerid)+'.ini'
    try:
        config.read(config_file_name)
        last_book_id = config['Recent']['book_id']
    except:
        last_book_id = "0"
        config['Recent'] = {'book_id': '0'}
        with open(config_file_name, 'w+') as configfile:
            config.write(configfile)

    for book in db.session.query(Books).order_by(asc(Books.id)).slice(start_id, end_id).all():
        if os.path.exists("stop"):
            log.info(f'Exit file existed. Worker id {workerid} ended!')
            return "Done!"
        log.info("book.id " + str(book.id))
        # log.info("book.slug " + str(book.slug))
        # log.info("book.author " + str(book.author))
        # log.info("book.category " + str(book.category))
        if book.id <= int(last_book_id):
            log.info(f'Book id {book.id} already posted. Skip!')
            continue
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
                    # log.debug("category_dict", category_dict)
                    category_id = post_category(category_dict)['id']
                category_ids.append(category_id)

            # log.debug("author_ids " + str(author_ids))
            # log.debug("category_ids " + str(category_ids))
            if book.status == "Đang ra":
                book_status = "Đang cập nhật"
            else:
                book_status = "Hoàn thành"
            #post feature image:
            try:
                media_id = get_image(book.slug)['id']
            except TypeError:
                media = {'file': open(os.path.join(media_path,f'{book.slug}.jpg'), 'rb'),
                         'slug': book.slug}
                media_id = post_image(media)['id']
            book_dict = {'title': book.name,
                    'status': 'publish',
                    'slug' : book.slug,
                    'content': book.description,
                    'tac-gia': ','.join([str(x) for x in author_ids]),
                    'categories' : ','.join([str(x) for x in category_ids]),
                    'tw_multi_chap' : '1',
                    'tw_status' : book_status,
                    'featured_media': media_id
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
            elif chapter_json['parent'] != book_json['id']:
                chapter_dict = {
                    'parent' : book_json['id'],
                    'slug': chapter_slug
                    }
                update_chapter(chapter_json['id'], chapter_dict)
                log.info(f"Update chapter's book id from {chapter_json['parent']} to {book_json['id']}")
            sleep(1)
            if os.path.exists("stop"):
                log.info(f'Exit file existed. Worker id {workerid} ended!')
                return "Done!"
        with open(config_file_name, 'w+') as configfile:
            config['Recent']['book_id'] = str(book.id)
            config.write(configfile)
    log.info(f'worker id {workerid} ended!')
    return "Done!"

start_book_id = 0
books_per_thread = 2066
#for i in range(10):
#    future = executor.submit(worker, i*books_per_thread, offset=books_per_thread)
# We can use a with statement to ensure threads are cleaned up promptly

with concurrent.futures.ThreadPoolExecutor(thread_name_prefix="Thread", max_workers=5) as executor:
    # Start the load operations and mark each future with its URL
    # future_to_url = {executor.submit(worker, start_book_id+workerid*books_per_thread, books_per_thread, workerid): workerid for workerid in range(4)}
    future_to_url = {
        executor.submit(worker, start_book_id + workerid * books_per_thread, books_per_thread, workerid): workerid for
        workerid in range(10)}
    for future in concurrent.futures.as_completed(future_to_url):
        workerid = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            log.error('%r generated an exception: %s' % (workerid, exc))
        else:
            log.info(f'Worker {workerid} finished!')

if os.path.exists("stop"):
    os.remove("stop")
log.info("All worker completed")
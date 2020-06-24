from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

# association table
book_category = Table('book_category', Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id')),
    Column('category_id', Integer, ForeignKey('categories.id'))
)

class Categories(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    slug = Column(String)
    url = Column(String)

    def __init__(self, name, slug, url):
        self.name = name
        self.slug = slug
        self.url = url

    def __repr__(self):
        return "<Categories('%s','%s', '%s')>" % (self.name, self.slug, self.url)

class Books(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    slug = Column(String)
    url = Column(String)
    author = Column(String)
    status = Column(String)
    thumbnail = Column(String)
    description = Column(Text)
    category = relationship("Categories", secondary=book_category, backref='categories')
    chapter = relationship("Chapters", backref="book")

    def __init__(self, name, slug, url, author, status, thumbnail):
        self.name = name
        self.slug = slug
        self.url = url
        self.author = author
        self.status = status
        self.thumbnail = thumbnail

    def __repr__(self):
        return "<Book('%s','%s', '%s, %s, %s')>" % (self.name, self.slug, self.url, self.author,self.status)

class Chapters(Base):
    __tablename__ = 'chapters'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    slug = Column(String)
    url = Column(String)
    book_id = Column(Integer, ForeignKey('books.id'))
    content = Column(Text)

    def __init__(self, name, slug, url, content):
        self.name = name
        self.slug = slug
        self.url = url
        self.content = content

    def __repr__(self):
        return "<Chapter('%s','%s', '%s')>" % (self.name, self.slug, self.url)
# from gettruyen.database.models import Categories, Books, Chapters, BookCategories
from models import Base

from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

import logging
import os

logging.basicConfig(level=logging.DEBUG)

# logger = logging.getLogger(__name__)
SQLITE = 'sqlite'
#Table Names

class TruyenFullDatabase:
    DB_ENGINE = {
        'sqlite' : 'sqlite:///{DB}'
    }

    #Main DB Connection Ref Obj
    db_engine = None
    def __init__(self, dbtype='sqlite', username='', password='', dbname='truyenfull.db'):
        dbtype = dbtype.lower()
        logging.debug('dbtype is %s' % dbtype)
        if dbtype in self.DB_ENGINE.keys():
            db_path = os.path.join(os.path.dirname(__file__), dbname)
            engine_url = self.DB_ENGINE[dbtype].format(DB=db_path)
            logging.debug("engine_url is %s" %engine_url)
            self.db_engine = create_engine(engine_url, connect_args={'check_same_thread':False}, echo=False)
            logging.debug(self.db_engine)
            self.metadata = MetaData()
            Session = sessionmaker(bind=self.db_engine)
            self.session = Session()
        else:
            print("DBType is not found in DB_ENGINE")
    def create_db_tables(self):
        try:
            Base.metadata.create_all(self.db_engine)
        except Exception as e:
            print("Error occurred during Table creation!")
            print(e)

    def insert_categories(self):
        from gettruyen.database.models import Categories
        genres = [
            Categories('Ngôn Tình', 'ngon-tinh', r"https://truyenfull.vn/the-loai/ngon-tinh/"),
            Categories('Đô Thị', 'do-thi', r"https://truyenfull.vn/the-loai/do-thi/"),
            Categories('Kiếm Hiệp', 'kiem-hiep', r"https://truyenfull.vn/the-loai/kiem-hiep/"),
            Categories('Quan Trường', 'quan-truong', r"https://truyenfull.vn/the-loai/quan-truong/"),
            Categories('Võng Du', 'vong-du', r"https://truyenfull.vn/the-loai/vong-du/"),
            Categories('Khoa Huyễn', 'khoa-huyen', r"https://truyenfull.vn/the-loai/khoa-huyen/"),
            Categories('Hệ Thống', 'he-thong', r"https://truyenfull.vn/the-loai/he-thong/"),
            Categories('Huyền Huyễn', 'huyen-huyen', r"https://truyenfull.vn/the-loai/huyen-huyen/"),
            Categories('Dị Giới', 'di-gioi', r"https://truyenfull.vn/the-loai/di-gioi/"),
            Categories('Dị Năng', 'di-nang', r"https://truyenfull.vn/the-loai/di-nang/"),
            Categories('Quân Sự', 'quan-su', r"https://truyenfull.vn/the-loai/quan-su/"),
            Categories('Lịch Sử', 'lich-su', r"https://truyenfull.vn/the-loai/lich-su/"),
            Categories('Xuyên Không', 'xuyen-khong', r"https://truyenfull.vn/the-loai/xuyen-khong/"),
            Categories('Trọng Sinh', 'trong-sinh', r"https://truyenfull.vn/the-loai/trong-sinh/"),
            Categories('Trinh Thám', 'trinh-tham', r"https://truyenfull.vn/the-loai/trinh-tham/"),
            Categories('Thám Hiểm', 'tham-hiem', r"https://truyenfull.vn/the-loai/tham-hiem/"),
            Categories('Linh Dị', 'linh-di', r"https://truyenfull.vn/the-loai/linh-di/"),
            Categories('Sắc', 'sac', r"https://truyenfull.vn/the-loai/sac/"),
            Categories('Ngược', 'nguoc', r"https://truyenfull.vn/the-loai/nguoc/"),
            Categories('Sủng', 'sung', r"https://truyenfull.vn/the-loai/sung/"),
            Categories('Cung Đấu', 'cung-dau', r"https://truyenfull.vn/the-loai/cung-dau/"),
            Categories('Nữ Cường', 'nu-cuong', r"https://truyenfull.vn/the-loai/nu-cuong/"),
            Categories('Gia Đấu', 'gia-dau', r"https://truyenfull.vn/the-loai/gia-dau/"),
            Categories('Đông Phương', 'dong-phuong', r"https://truyenfull.vn/the-loai/dong-phuong/"),
            Categories('Đam Mỹ', 'dam-my', r"https://truyenfull.vn/the-loai/dam-my/"),
            Categories('Bách Hợp', 'bach-hop', r"https://truyenfull.vn/the-loai/bach-hop/"),
            Categories('Hài Hước', 'hai-huoc', r"https://truyenfull.vn/the-loai/hai-huoc/"),
            Categories('Điền Văn', 'dien-van', r"https://truyenfull.vn/the-loai/dien-van/"),
            Categories('Cổ Đại', 'co-dai', r"https://truyenfull.vn/the-loai/co-dai/"),
            Categories('Mạt Thế', 'mat-the', r"https://truyenfull.vn/the-loai/mat-then/"),
            Categories('Truyện Teen', 'truyen-teen', r"https://truyenfull.vn/the-loai/truyen-teen/"),
            Categories('Phương Tây', 'phuong-tay', r"https://truyenfull.vn/the-loai/phuong-tay/"),
            Categories('Nữ Phụ', 'nu-phu', r"https://truyenfull.vn/the-loai/nu-phu/"),
            Categories('Light Novel', 'light-novel', r"https://truyenfull.vn/the-loai/light-novel/"),
            Categories('Việt Nam', 'viet-nam', r"https://truyenfull.vn/the-loai/viet-nam/"),
            Categories('Đoản Văn', 'doan-van', r"https://truyenfull.vn/the-loai/doan-van/"),
            Categories('Tiên Hiệp', 'tien-hiep', r"https://truyenfull.vn/the-loai/tien-hiep/"),
            Categories('Xuyên Nhanh', 'xuyen-nhanh', r"https://truyenfull.vn/the-loai/xuyen-nhanh/"),
            Categories('Khác', 'khac', r"https://truyenfull.vn/the-loai/khac/"),
        ]
        for _genre in genres:
            if self.session.query(Categories).filter(Categories.url == _genre.url).first() is None:
                self.session.add(_genre)
        self.session.commit()
    def print_categories(self):
        from gettruyen.database.models import Categories
        results = self.session.query(Categories)
        for row in results:
            print(row)
if __name__ == "__main__":
    db = TruyenFullDatabase(SQLITE, dbname='truyenfull.db')
    db.create_db_tables()
    db.insert_categories()
    db.print_categories()
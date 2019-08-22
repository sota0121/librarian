import sqlite3
from contextlib import closing
import pandas as pd

#=========================================================
# 蔵書データベース管理クラス
# CRUDを担う
#=========================================================
# https://gray-code.com/php/create-table-by-using-sqlite3/
# https://www.dbonline.jp/sqlite/table/index9.html#section1
# https://qiita.com/mas9612/items/a881e9f14d20ee1c0703
# https://qiita.com/inon3135/items/515bd3fae4fc66e28ed8
# https://blog.amedama.jp/entry/sqlite3-in-memory-issue
# https://stackoverflow.com/questions/5801170/python-sqlite-create-table-if-not-exists-problem
# https://riptutorial.com/ja/pandas/example/5586/%E3%82%BF%E3%83%97%E3%83%AB%E3%81%AE%E3%83%AA%E3%82%B9%E3%83%88%E3%81%8B%E3%82%89dataframe%E3%82%92%E4%BD%9C%E6%88%90%E3%81%99%E3%82%8B
#---------------------------------------------------------

class bookdb:
    
    def __init__(self,dbname="database.db"):
        self.database_name = dbname
        self.conn = sqlite3.connect(dbname)
        self.c = self.conn.cursor()
    
    def __del__(self):
        self.c.close()
        self.conn.close()

    def create_table(self, tablename="books"):
        query = 'create table if not exists ' + tablename + ' ('
        query += 'unique_id INTEGER PRIMARY KEY, '
        query += 'isbn TEXT NOT NULL, '
        query += 'title TEXT NOT NULL, '
        query += 'status INTEGER'
        query += ');'
        self.c.execute(query)
        print(query)
        self.conn.commit()

    # Insert a record
    def insert_book_record(self, isbn="0000000000000", title="default", status=0):
        # SQL文に値をセットする場合は，Pythonのformatメソッドなどは使わずに，
        # セットしたい場所に?を記述し，executeメソッドの第2引数に?に当てはめる値を
        # タプルで渡す．
        query = 'insert into books (isbn, title, status) values (?,?,?)'
        bookinfo = (isbn, title, status)
        self.c.execute(query, bookinfo)
        self.conn.commit()
    
    # Insert records
    #  > books is list of touple like this >> [(isbn,title,status),(),()...]
    def insert_book_records(self, books=[]):
        query = 'insert into books (isbn, title, status) values (?,?,?)'
        self.c.executemany(query, books)
        self.conn.commit()

    # Test Read DB
    def select_table_alldata_as_df(self, tablename="books"):
        query = 'select * from ' + tablename
        records = []
        for rec in self.c.execute(query):
            records.append(rec)
        
        df = pd.DataFrame(records)
        return df




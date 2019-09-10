import sqlite3
import pandas as pd

# =========================================================
# 蔵書データベース管理クラス
# CRUDを担う
# =========================================================
# https://gray-code.com/php/create-table-by-using-sqlite3/
# https://www.dbonline.jp/sqlite/table/index9.html#section1
# https://qiita.com/mas9612/items/a881e9f14d20ee1c0703
# https://qiita.com/inon3135/items/515bd3fae4fc66e28ed8
# https://blog.amedama.jp/entry/sqlite3-in-memory-issue
# https://stackoverflow.com/questions/5801170/python-sqlite-create-table-if-not-exists-problem
# https://riptutorial.com/ja/pandas/example/5586/%E3%82%BF%E3%83%97%E3%83%AB%E3%81%AE%E3%83%AA%E3%82%B9%E3%83%88%E3%81%8B%E3%82%89dataframe%E3%82%92%E4%BD%9C%E6%88%90%E3%81%99%E3%82%8B
# https://pythondatascience.plavox.info/pandas/%E8%A1%8C%E3%83%BB%E5%88%97%E3%81%AE%E6%8A%BD%E5%87%BA
# https://pythondatascience.plavox.info/pandas/%E8%A1%8C%E3%83%BB%E5%88%97%E3%81%AE%E9%95%B7%E3%81%95%E3%82%92%E7%A2%BA%E8%AA%8D
# ---------------------------------------------------------

# -----------------------------------
# DB Architect
#  - column0 : unique id
#  - column1 : isbn
#  - column2 : title
#  - column3 : status
# ***********
# status
# 0 : avalable(利用可能)
# 1 : checked out(貸出中)
# 2 : disposed(廃棄済)
# ***********
# -----------------------------------


class BookDB:
    def __init__(self, dbname="database.db"):
        self.database_name = dbname
        self.conn = sqlite3.connect(dbname)
        self.c = self.conn.cursor()

    def __del__(self):
        self.c.close()
        self.conn.close()

    # if table does not exists, create
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

    # Select all data with tablename
    def select_table_alldata_as_df(self, tablename="books"):
        query = 'select * from ' + tablename
        records = self.c.execute(query).fetchall()
        if records is None:
            return None
        df = pd.DataFrame(records)
        return df

    # Select last N data with tablename
    def select_table_lastNdata_as_df(self, tablename="books", datanum=0):
        # check args
        if datanum == 0:
            return None
        # check data num
        alldata = self.select_table_alldata_as_df(tablename)
        all_row_size = len(alldata.index)
        if (all_row_size == 0) or (all_row_size < datanum):
            return None
        # get last N data
        target_data = alldata[(all_row_size - 1 - datanum):(all_row_size - 1)]
        return target_data

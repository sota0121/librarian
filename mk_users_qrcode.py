# librarian.db - users table
# から各ユーザーのQRコード画像ファイルを生成するbatchツール

import sqlite3
import pandas as pd
import qrcode
import pathlib

# users table colomun names
# col0 : id (NotNULL, PK, Unique)
# col1 : name_jp
# col2 : name_en
ID_COL_IDX = 0
NAMEJP_COL_IDX = 1
NAMEEN_COL_IDX = 2
USERS_QRCODE_DIR = "./users_qrcode"


class UserDB:
    def __init__(self, dbname="librarian.db"):
        self.db_name = dbname
        self.conn = sqlite3.connect(dbname)
        self.c = self.conn.cursor()

    def __del__(self):
        self.c.close()
        self.conn.close()

    def select_user_tbl(self, tablename="users"):
        query = 'select * from ' + tablename
        records = self.c.execute(query).fetchall()
        if records is None:
            print("[Error]failed to select users table ...")
            return None
        df = pd.DataFrame(records)
        return df


def main():
    # open db and select users table
    db = UserDB()
    user_tbl = db.select_user_tbl()

    # prepare to output
    p = pathlib.Path(USERS_QRCODE_DIR)
    if p.exists() is False:
        p.mkdir()

    # make qrcode and save as png
    for ridx in range(len(user_tbl)):
        # id > qrcode
        qrcodestr = str(user_tbl[ID_COL_IDX][ridx])
        qrcodeimg = qrcode.make(qrcodestr)
        # namejp > qrcode filename
        imgfname = str(user_tbl[NAMEJP_COL_IDX][ridx]) + '.png'
        qrcodeimg.save(USERS_QRCODE_DIR + '/' + imgfname)
        # debug code
        print('saved code :' + qrcodestr + ', fname :' + imgfname)


if __name__ == "__main__":
    main()

# 新規購入書籍をDBに登録するアプリケーション
# https://note.nkmk.me/python-pillow-qrcode/
# https://note.nkmk.me/python-pandas-dataframe-for-iteration/
# https://qiita.com/Kenta-Han/items/e64035e9c3e4ef08e394#%E6%96%87%E5%AD%97%E5%88%97%E3%81%AE%E5%88%87%E3%82%8A%E5%87%BA%E3%81%97

import requests
from codereader import CodeReader
from bookdb import BookDB
import qrcode
import pathlib


class RegisterBooks:
    BOOK_DB_NAME = "book_database.db"
    GBOOKS_API_URL = 'https://www.googleapis.com/books/v1/volumes?q=isbn:'
    QR_CODE_IMG_DIR = './qrcode_files'

    def __init__(self):
        self.reader = CodeReader()
        self.db = BookDB(RegisterBooks.BOOK_DB_NAME)
        self.db.create_table()
        outdir = pathlib.Path(RegisterBooks.QR_CODE_IMG_DIR)
        if not outdir.exists():
            outdir.mkdir()

    # def __del__(self):
    #     pass

    def search_book_with_isbn(self, isbn):
        req_url = RegisterBooks.GBOOKS_API_URL + str(isbn)
        response = requests.get(req_url)
        return response

    def get_booktitle_from_gbsapi(self, json_data):
        try:
            title = json_data['items'][0]['volumeInfo']['title']
        except:
            title = None
        return title

    def print_start_msg(self):
        print("")
        print("Register New Books for book database.")
        print("step1 : Scan new books over and over")
        print("step2 : push ESC key to save and quit")
        print("------")
        print(">>> NOTE1 ")
        print(">>> - if failed to get isbncode with scaning book,")
        print(">>> - input isbncode with keyboard, please.")
        print(">>> NOTE2 ")
        print(">>> - if failed to get book info from Web,")
        print(">>> - input book title with keyboard, please.")
        print("")
        print("")

    # main process loop until input ESC
    def start(self):
        # ===========================================================
        # scanning books and getting books' info phase
        # ===========================================================
        registerd_count = 0
        self.print_start_msg()
        while True:
            # ----------------------------------------------------
            # Get ISBN code
            # ----------------------------------------------------
            ret, code = self.reader.read()
            # カメラからISBNコードをとれない場合は手入力
            if ret == -1:
                print("input isbn code with keyboard ...")
                print("NOTE : isbn consists of 13 numbers")
                code = input()
            # ESCを押したら保存せずにアプリケーションを終了
            elif ret == -2:
                print("save and quit ... ")
                break
            # ----------------------------------------------------
            # Get Book's info with ISBN code
            # ----------------------------------------------------
            response = self.search_book_with_isbn(code)
            json_data = response.json()
            book_title = self.get_booktitle_from_gbsapi(json_data)
            # APIから本のタイトルが取得できない場合は手入力
            if book_title is None:
                print('sorry cant find that book ... isbn = ' + str(code))
                print('input book title , please.')
                book_title = input()
            # 登録する情報を表示する
            print("isbn: " + str(code) + ", title: " + str(book_title))

            # ----------------------------------------------------
            # Register for DB
            # ----------------------------------------------------
            self.db.insert_book_record(
                isbn=str(code), title=book_title, status=0)
            registerd_count += 1

        # ===========================================================
        # generate book's unique QR code image
        # ===========================================================
        registered_data = self.db.select_table_lastNdata_as_df(datanum=registerd_count)
        if registered_data is None:
            return
        for row in registered_data.itertuples():
            # QR code string
            qrcode_str = str(row[1]) + "_" + str(row[2])
            # QR code image file name
            title_str = str(row[3]).strip()[:10]
            qrcode_filename = str(row[1]) + "_" + title_str + ".png"
            # output QR code png file
            qrcode_img = qrcode.make(qrcode_str)
            qrcode_img.save(RegisterBooks.QR_CODE_IMG_DIR + '/' + qrcode_filename)
            # debug code
            print(row)


if __name__ == "__main__":
    app = RegisterBooks()
    app.start()

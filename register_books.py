####################################################
# function
# - 本のバーコードを撮影する
# - バーコードからISBNコード(13桁)を読み取る
# - 読み取ったコードをGoogleBooksAPIで検索する
# - APIのresponse(json)からタイトルを取得する
# - id, isbn, title, unique_id をDBに登録
# - 登録した内容をCSV形式で保存
# - 次回実行時は続きから作業可能
####################################################
import os
import time
import json
import re
import math
import csv
import platform
import numpy as np
import pandas as pd
import requests
import cv2
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol


#==============================================================
# http://peaceandhilightandpython.hatenablog.com/entry/2016/01/08/000857
# https://qiita.com/wakaba130/items/3a9f0dd23dfacc5b4602
# https://qiita.com/ryu19maki/items/e5a3b470795de883a09a

class TestRegisterBook:
    def __init__(self):
        self.url = 'https://www.googleapis.com/books/v1/volumes?q=isbn:'
        self.cur_unique_id = 0

    # CSV形式でログ出力
    def OutputCodes(self, codes):
        """
            isbnコードをログファイルに出力する
            column 0 : index
            column 1 : isbn code
        """
        indices = []
        for i in range(len(codes)):
            indices.append(i)

        s = pd.Series(codes, index=indices)
        print(s)
        s.to_csv('./log_isbn.csv')

    def search_with_isbn(self, isbn):
        req_url = self.url + isbn
        response = requests.get(req_url)
        return response

    def get_title_gbsapi(self, json_data):
        try:
            title = json_data['items'][0]['volumeInfo']['title']
        except:
            title = None
        return title

    def beep(self, freq, dur=100):
        """
            ビープ音を鳴らす.
            @param freq 周波数
            @param dur  継続時間（ms）
        """
        if platform.system() == "Windows":
            # Windowsの場合は、winsoundというPython標準ライブラリを使います.
            import winsound
            winsound.Beep(freq, dur)
        else:
            # Macの場合には、Macに標準インストールされたplayコマンドを使います.
            import os
            os.system('play -n synth %s sin %s' % (dur/1000, freq))

    def contrast(self, image, a):
        lut = [ np.uint8(255.0 / (1 + math.exp(-a * (i - 128.) / 255.))) for i in range(256)]
        result_image = np.array( [ lut[value] for value in image.flat], dtype=np.uint8 )
        result_image = result_image.reshape(image.shape)
        return result_image
        
    def convert_image_to_code(self, image):
        isbnNumber = ""
        allCodes = decode(image, symbols=[ZBarSymbol.EAN13])
        if len(allCodes) > 0: # Barcode was detected
                for code in allCodes:
                    codesStr = str(code)
                    isbnPattern = r"9784\d+"
                    isbnSearchOB = re.search(isbnPattern,codesStr)
                    if isbnSearchOB: # ISBN was detected
                        if isbnNumber != isbnSearchOB.group(): # New ISBN was detected
                            isbnNumber = isbnSearchOB.group()

                            return isbnNumber
        else:
            return -1

    # 予定：DBを用いて実装するようにリファクタリングする
    def makeUniqueID(self):
        self.cur_unique_id += 1
        return (self.cur_unique_id - 1)

    def main(self):
        # post process
        capture = cv2.VideoCapture(0) # カメラ番号を選択、例えば　capture = cv2.VideoCapture(1)
        if capture.isOpened() is False:
            raise("IO Error")
        cv2.namedWindow("Capture", cv2.WINDOW_AUTOSIZE)
        
        # main loop for reading barcode
        print('main loop ... \n\n')
        isbn_codes = []
        book_titles = []
        unique_ids = []
        target = (240,140,440,340) #L-T-R-B
        while True:
            ret, image = capture.read()
            image_mirror = cv2.flip(image, 1)
            image_mirror_r = cv2.rectangle(image_mirror,(target[2], target[3]), (target[0], target[1]),(200,200,0),3)
            if ret == False:
                continue
            # GrayScale
            imageGlay = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            image = self.contrast(imageGlay, 5)

            # Show image
            cv2.imshow("Capture", image_mirror_r )

            # image to code
            roi = image[target[1]: target[3], target[0]: target[2]]
            isbn_code = self.convert_image_to_code(roi)
            
            # get book title with Google Books API
            if isbn_code == None:
                print("sorry cant convert image to code ... ")
                continue
            elif isbn_code != -1 :
                self.beep(1000, 300) # successed in capturing
                # get book's title
                response = self.search_with_isbn(isbn_code)
                json_data = response.json()
                book_title = self.get_title_gbsapi(json_data)
                if book_title == None:
                    print('sorry cant find that book ... isbn = ' + str(isbn_code) )
                    continue
                # print
                print("isbn:" + str(isbn_code) + ", title:" + str(book_title))
                # register
                unique_ids.append(self.makeUniqueID())
                isbn_codes.append(isbn_code)
                book_titles.append(book_title)
                # just a moment sleep
                time.sleep(1.0)

            keyInput = cv2.waitKey(3) # 撮影速度 大きくなると遅くなる
            if keyInput == 27: # when ESC
                break
        
        capture.release()
        cv2.destroyAllWindows()

        # log
        print('\n\nOutput data ... ')
        s_uid = pd.Series(unique_ids)
        s_isbn = pd.Series(isbn_codes)
        s_title = pd.Series(book_titles)
        outputdf = pd.concat([s_uid, s_isbn, s_title], axis=1)
        outputdf.columns = ['UNIQUE_ID', 'ISBN', 'TITLE']
        outputdf.to_csv('registered_db.csv', index=False)
        print('Terminate Process ... Bye!!')


if __name__ == "__main__":
    obj = TestRegisterBook()
    obj.main()



import cv2
import pandas as pd
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol
import re
import numpy as np
import math
import os
import platform
import csv
import time

# https://note.nkmk.me/python-pandas-list/
# https://note.nkmk.me/python-pandas-to-csv/
# https://pypi.org/project/pyzbar/

#####################################################
# 機能
#   - ISBNバーコードをWebカメラ(id=0)で撮影
#   - ISBNバーコードを認識(ESCを押すまで繰り返す)
#   - 終了ボタン(ESC)でそれまでに記録したISBNを出力
#####################################################

# CSV形式でログ出力
def OutputCodes(codes):
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
    

def beep(freq, dur=100):
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

def contrast(image, a):
    lut = [ np.uint8(255.0 / (1 + math.exp(-a * (i - 128.) / 255.))) for i in range(256)]
    result_image = np.array( [ lut[value] for value in image.flat], dtype=np.uint8 )
    result_image = result_image.reshape(image.shape)
    return result_image
       
def convert_image_to_code(image):
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


def main():
    # post process
    capture = cv2.VideoCapture(0) # カメラ番号を選択、例えば　capture = cv2.VideoCapture(1)
    if capture.isOpened() is False:
        raise("IO Error")
    cv2.namedWindow("Capture", cv2.WINDOW_AUTOSIZE)
    
    # main loop for reading barcode
    print('main loop ... \n\n')
    codes = []
    while True:
        ret, image = capture.read()
        image_mirror = cv2.flip(image, 1)
        if ret == False:
            continue
        # GrayScale
        imageGlay = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = contrast(imageGlay, 5)

        # Show image
        cv2.imshow("Capture", image_mirror )

        # image to code
        code = convert_image_to_code(image)
        if code == None:
            sp = "skip this ... " + str(code)
            print(sp)
            continue
        elif code != -1:
            s_code = str(code)
            beep(1000, 300)
            print(code)
            codes.append(s_code)
            time.sleep(1.0)
            

        keyInput = cv2.waitKey(3) # 撮影速度 大きくなると遅くなる
        if keyInput == 27: # when ESC
            break
    
    capture.release()
    cv2.destroyAllWindows()

    # log
    print('\n\nOutput codes ... ')
    if len(codes) > 0:
        OutputCodes(codes)
    print('Terminate Process ... Bye!!')


if __name__ == '__main__':
    main()
    


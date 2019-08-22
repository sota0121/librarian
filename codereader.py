# 本のISBNコードを取得するクラス
# 読み取りデバイスはカメラ、バーコードリーダー、QRコードリーダー
# いずれになっても問題ないようにラッパーの役割を果たす

import math
import numpy as np
import platform
import cv2
import re
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol

class CodeReader:
    PLATFORM_SYSTEM = "Windows"
    BEEP_FREQ = 1000
    BEEP_DUR = 300
    TARGET_RECT = (240,140,440,340) #L-T-R-B
    
    def __init__(self):
        self.capture = cv2.VideoCapture(0)
        if self.capture.isOpened() is False:
            raise("Failed to Video Capture ...")
        cv2.namedWindow("Capture", cv2.WINDOW_AUTOSIZE)
    
    def __del__(self):
        self.capture.release()
        cv2.destroyAllWindows()
    
    # beep
    def beep(self):
        """
            ビープ音を鳴らす.
            @param freq 周波数
            @param dur  継続時間（ms）
        """
        if platform.system() == CodeReader.PLATFORM_SYSTEM:
            # Windowsの場合は、winsoundというPython標準ライブラリを使います.
            import winsound
            winsound.Beep(CodeReader.BEEP_FREQ, CodeReader.BEEP_DUR)
        else:
            # Macの場合には、Macに標準インストールされたplayコマンドを使います.
            import os
            os.system('play -n synth %s sin %s' % (CodeReader.BEEP_DUR/1000, CodeReader.BEEP_FREQ))
    
    # contrast image
    def contrast(self, image, a):
        lut = [ np.uint8(255.0 / (1 + math.exp(-a * (i - 128.) / 255.))) for i in range(256)]
        result_image = np.array( [ lut[value] for value in image.flat], dtype=np.uint8 )
        result_image = result_image.reshape(image.shape)
        return result_image

    # convert image to isbn code(13 numbers)
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

    # Show image
    def show_image(self):
        ret, image = self.capture.read()
        image_mirror = cv2.flip(image, 1)
        image_mirror_r = cv2.rectangle(image_mirror,(CodeReader.TARGET_RECT[2], CodeReader.TARGET_RECT[3]), (CodeReader.TARGET_RECT[0], CodeReader.TARGET_RECT[1]),(200,200,0),3)
        if ret == False:
            return (-1), image
        cv2.imshow("Capture", image_mirror_r)
        return (0), image

    # Scan Code > output : isbn code
    def scan_book(self, image):
        imageGlay = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = self.contrast(imageGlay, 5)
        roi = image[CodeReader.TARGET_RECT[1]: CodeReader.TARGET_RECT[3], CodeReader.TARGET_RECT[0]: CodeReader.TARGET_RECT[2]]
        isbncode = self.convert_image_to_code(roi)
        return isbncode

    # Main Proccess
    # ret0 : success:0, failed:-1, quit:-2
    # ret1 : isbncode(INT)
    def read(self):
        print("-----------------------------------------")
        print("> Scan book barcode")
        print("-----------------------------------------")
        print("...")
        while True:
            ret, img = self.show_image()
            if ret == -1:
                print("")
                continue
            
            isbn_code = self.scan_book(img)
            if isbn_code == None:
                print("sorry cant convert image to code ... ")
                return (-1), (-1)
            elif isbn_code != -1:
                self.beep()
                print("isbn: " + str(isbn_code))
                return 0, isbn_code
            
            keyinput = cv2.waitKey(3)
            if keyinput == 27: #ESC
                return (-2), (-1)
            elif keyinput == ord('s'): #'S' key
                return (1), (-1)









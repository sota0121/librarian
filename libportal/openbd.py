import json, requests, os

# PATH
result_html = 'result.html'
result_template = 'views/template.tpl'
book_json = 'book.json'

# result.htmlに吐き出す
def out_html(book_data_list):
    temp_data = ''
    with open(result_template, 'r', encoding='utf-8') as r_file:
        for line_data in r_file:
            temp_data += line_data
    data = temp_data.format(
        book_data_list[5],  # Cover
        book_data_list[1],  # タイトル
        book_data_list[2],  # 著者
        book_data_list[3],  # 出版社
        book_data_list[4],  # 発売日
        book_data_list[0])  # ISBN
    file = open(result_html, 'w', encoding='utf-8')
    file.write(data)

# 詳細データから必要事項を取得
def getNeedData():
    file = open(book_json, 'r', encoding='utf-8')
    dict_json = json.load(file)
    if dict_json[0] == None:
        print('ISBNが不正です')
    else:
        # ISBN, title, 著者, 出版社, 発売日, CoverPhoto
        label = ['isbn', 'title', 'author', 'publisher', 'pubdate', 'cover']
        book_Data = []
        for i in range(len(label)):
            book_Data.append(dict_json[0]['summary'][label[i]])
        # os.system('wget -O sample.jpg {}'.format(_book_Data[5]))
        out_html(book_Data)
        return book_Data

# ISBNからデータ取得
def getBookData(isbn):
    url = 'http://api.openbd.jp/v1/get?isbn={}&pretty'.format(isbn)
    response = (requests.get(url)).text
    file = open(book_json, 'w', encoding='utf-8')
    file.write(response)

if __name__ == '__main__':
    isbn = input('ISBN：')
    getBookData(isbn)
    getNeedData()

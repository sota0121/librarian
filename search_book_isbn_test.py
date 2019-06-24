# Ref ===============================================
# https://qiita.com/seihmd/items/4cafe204403ac2889145
# https://techracho.bpsinc.jp/katayama-yuuki/2018_01_29/51416
# https://qiita.com/TakeshiNickOsanai/items/2d9c30cedcba21f36669
# http://toricor.hatenablog.com/entry/2016/01/16/160406
# https://qiita.com/Morio/items/5170c103647ef3a4aa69
# https://note.nkmk.me/python-pandas-list/
# https://note.nkmk.me/python-pandas-concat/
# https://note.nkmk.me/python-pandas-dataframe-rename/


####################################################
# Google Books API を用いて本を検索する
# ISBNコード(13桁)を使う
####################################################
import requests
import json
import pandas as pd

url = 'https://www.googleapis.com/books/v1/volumes?q=isbn:'

def search_with_isbn(isbn):
    req_url = url + isbn
    response = requests.get(req_url)
    return response

def get_title_gbsapi(json_data):
    try:
        title = json_data['items'][0]['volumeInfo']['title']
    except:
        title = None
    return title

if __name__ == "__main__":
    isbn_codes = []
    book_titles = []
    indices = []
    i = 0
    while True:
        # user input
        isbn_input = input("input ISBN >>>")
        if isbn_input == "0":
            break
        
        # search
        response = search_with_isbn(isbn_input)

        # parse json
        json_data = response.json()
        book_title = get_title_gbsapi(json_data)
        if book_title == None:
            print('sorry cant find that book ... ')
            continue

        # append
        isbn_codes.append(isbn_input)
        book_titles.append(book_title)
        indices.append(i)
        i += 1
    
    ## output
    s_isbn = pd.Series(isbn_codes)
    s_title = pd.Series(book_titles)
    outputdf = pd.concat([s_isbn, s_title], axis=1)
    outputdf.columns = ['ISBN', 'TITLE']
    outputdf.to_csv('search_results.csv')

    






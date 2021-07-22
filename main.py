""" 동아일보 특정 키워드를 포함하는, 특정 날짜 이전 기사 내용 크롤러(정확도순 검색)
    python [모듈 이름] [키워드] [가져올 페이지 숫자] [결과 파일명]
    한 페이지에 기사 15개
"""

import sys
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import quote
import csv
import re

TARGET_URL_BEFORE_PAGE_NUM = "http://news.donga.com/search?p="
TARGET_URL_BEFORE_KEWORD = '&query='
TARGET_URL_REST = '&check_news=1&more=1&sorting=3&search_date=1&v1=&v2=&range=3'


# 기사 검색 페이지에서 기사 제목에 링크된 기사 본문 주소 받아오기
def get_link_from_news_title(start_page, end_page, URL, output_file):
    for i in range(start_page, end_page):
        current_page_num = 1 + i*15
        position = URL.index('=')
        URL_with_page_num = URL[: position+1] + str(current_page_num) \
                            + URL[position+1 :]
        source_code_from_URL = urllib.request.urlopen(URL_with_page_num)
        soup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')

        for title in soup.find_all('p', 'tit'):
            news_title = []
            title_link = title.select('a')
            # print("title: ", str(title.find_all(text=True)))
            name = str(title.find_all(text=True))
            name = clean_text(name)
            news_title.append(name)
            # print("title link: ", title.txt)
            article_URL = title_link[0]['href']  # 기사 링크
            results = get_text(article_URL, output_file, news_title)

            for i in results:
                output_file.writerow(i)


# 기사 본문 내용 긁어오기 (위 함수 내부에서 기사 본문 주소 받아 사용되는 함수)
def get_text(URL, output_file, news_title):
    source_code_from_url = urllib.request.urlopen(URL)
    soup = BeautifulSoup(source_code_from_url, 'lxml', from_encoding='utf-8')
    content_of_article = soup.select('div.article_txt')
    # print(content_of_article)
    results = []
    # print("==========", content_of_article)
    temp = []
    for item in content_of_article:
        txt = str(item.find_all(text=True))
        txt = clean_text(txt)
        string_item = txt
        #string_item = clean_text(string_item)
    temp.append(news_title)
    temp.append(string_item)
    results.append(temp)
    return results


def clean_text(text):
    cleaned_text = re.sub('[a-zA-Z]', '', text)
    cleaned_text = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"▲□■◇]',
                          '', cleaned_text)
    return cleaned_text


# 메인함수
def main(argv):
    if len(argv) != 5:
        print("python [모듈이름] [키워드] [시작 페이지 숫자] [끝 페이지 숫] [결과 파일명]")
        return
    keyword = argv[1]
    start_page = int(argv[2])
    end_page = int(argv[3])
    output_file_name = argv[4]
    target_URL = TARGET_URL_BEFORE_PAGE_NUM + TARGET_URL_BEFORE_KEWORD \
                 + quote(keyword) + TARGET_URL_REST
    f = open(output_file_name, 'w', encoding='utf-8-sig')
    output_file = csv.writer(f)
    get_link_from_news_title(start_page, end_page, target_URL, output_file)
    f.close()


if __name__ == '__main__':
    main(sys.argv)

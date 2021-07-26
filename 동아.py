import sys
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import quote
import csv
import re
from urllib.request import Request, urlopen

TARGET_URL_BEFORE_PAGE_NUM = "https://search.naver.com/search.naver?where=news&sm=tab_pge"
TARGET_URL_BEFORE_KEWORD = '&query='
TARGET_URL_REST = '&sort=1&photo=0&field=0&pd=3&ds=2019.11.01&de=2020.10.28&mynews=1&office_type=1&office_section_code=1&news_office_checked='
TARGET_END = '&nso=so:dd,p:from20191101to20201028,a:all&start='


# 기사 검색 페이지에서 기사 제목에 링크된 기사 본문 주소 받아오기
def get_link_from_news_title(URL, output_file, target):
    for i in range(400):
        print("iiiiiii", i)
        current_page_num = 1 + i * 10
        position = URL.index('=')
        URL_with_page_num = URL[: position+1] + URL[position+1 :] + str(current_page_num)
        source_code_from_URL = urllib.request.urlopen(URL_with_page_num)
        # print(URL_with_page_num)
        soup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')
        #

        for title in soup.find_all('div', 'news_area'):
            # print("aaaaaa", title.find_all('a', 'info'))
            news_title = []
            title_link = title.select('a')
            #print("testtest ", date)
            #title_link = title.select('a', 'news_tit')
            # print("fdfdfddfd", title_link)
            link = title_link[5]['href']
            name = title_link[5]['title']
            news_title = clean_text(name)
            #print("news_title : ", news_title)
            article_URL = link  # 기사 링크
            #print("기사 링크 : ", article_URL)

            results = donga_get_text(article_URL, output_file, news_title)

            for result in results:
                output_file.writerow(result)

            #return False


def donga_get_text(URL, output_file, news_title):
    # OK
    URL += "#replyLayer"
    # print(URL)
    source_code_from_url = urllib.request.urlopen(URL)
    soup = BeautifulSoup(source_code_from_url, 'lxml', from_encoding='utf-8')
    content_of_article = soup.select('#content > div > div.article_txt')
    #print(soup)
    comments = soup.select('#spinTopLayerCommentList > li:nth-child(1) > div.module > div.comment')
    date = soup.select('#container > div.article_title > div.title_foot > span:nth-child(3)')
    date = str(date).split(" ")[2]


    #comments = soup.select('')
    #print('comments', comments)
    results = []
    temp = []
    txt = ""
    comment = ""
    for item in content_of_article:
        txt = str(item.find_all(text=True))
        txt = clean_text(txt)

    for com in comments:
        comment = str(com.find_all(text=True))
        comment = clean_text(comment)
        #print(comment)

    temp.append(date)
    temp.append(news_title)
    temp.append(txt)
    temp.append(comment)
    temp.append(URL)
    results.append(temp)
    return results


def clean_text(text):
    cleaned_text = re.sub('[a-zA-Z]', '', text)
    cleaned_text = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"▲□■◇]', '', text)
    cleaned_text = cleaned_text.replace('n ', '')
    return cleaned_text


# 메인함수
def main(argv):
    if len(argv) != 3:
        print("python [모듈이름] [키워드] [결과 파일명]")
        return

    keyword = argv[1]
    output_file_name = argv[2]
    target = "1020"
    target_URL = TARGET_URL_BEFORE_PAGE_NUM + TARGET_URL_BEFORE_KEWORD + quote(keyword) + TARGET_URL_REST + target + TARGET_END
    f = open(output_file_name, 'w', encoding='utf-8-sig')
    row = ['날짜', '기사제목', '본문', '댓글', '링크']
    output_file = csv.writer(f)
    output_file.writerow(row)
    get_link_from_news_title(target_URL, output_file, target)
    f.close()


if __name__ == '__main__':
    main(sys.argv)


import sys
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import quote
import csv
import re
from urllib.request import Request, urlopen

TARGET_URL_BEFORE_PAGE_NUM = "https://search.naver.com/search.naver?where=news&sm=tab_pge"
TARGET_URL_BEFORE_KEWORD = '&query='
TARGET_URL_REST = '&sort=1&photo=0&field=0&pd=3&ds=2019.11.01&de=2020.12.31&mynews=1&office_type=1&office_section_code=1&news_office_checked='
TARGET_END = '&nso=so:dd,p:from20191101to20201231,a:all&start='


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

            results = hani_get_text(article_URL, output_file, news_title)

            for result in results:
                output_file.writerow(result)

        #return False


def hani_get_text(URL, output_file, news_title):
    req = Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
    source_code_from_url = urlopen(req).read()
    # print('source_code_from_url', source_code_from_url)
    print(URL)
    soup = BeautifulSoup(source_code_from_url, 'lxml', from_encoding='utf-8')
    date = soup.select('#article_view_headline > p.date-time > span:nth-child(2)')
    #print('date1 :', date)
    #date = str(date).split(' ')[1][6:]
    #print('date :', date)

    results = []
    temp = []
    txt = ""
    comment = ""
    # 제목
    content_of_article = soup.select('div.subject')
    for item in content_of_article:
        string_item = str(item.find_all(text=True))
        #print(string_item)

    # 본문
    contents = soup.select('div.article-text > div > div.text')
    for item in contents:
        txt = str(item.find_all(text=True))
        txt = clean_text(txt)
        #print('string_item', string_item)

    # 댓글
    comments = soup.select('#list > div.reply-wrapper.reply-best-wrapper > div.reply-bottom > div.reply-content-wrapper')
    #print(comments)
    for com in comments:
        com = str(com.find_all(text=True))
        #print('com : ', com)

    temp.append(date)
    temp.append(news_title)
    temp.append(txt)
    temp.append(comment)
    temp.append(URL)
    results.append(temp)
    return results


def clean_text(text):
    # cleaned_text = re.sub('[a-zA-Z]', '', text)
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
    target = "1028"
    target_URL = TARGET_URL_BEFORE_PAGE_NUM + TARGET_URL_BEFORE_KEWORD + quote(keyword) + TARGET_URL_REST + target + TARGET_END
    f = open(output_file_name, 'w', encoding='utf-8-sig')
    row = ['날짜', '기사제목', '본문', '댓글', '링크']
    output_file = csv.writer(f)
    output_file.writerow(row)
    get_link_from_news_title(target_URL, output_file, target)
    f.close()


if __name__ == '__main__':
    main(sys.argv)

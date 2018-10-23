import requests
import time
from bs4 import BeautifulSoup

def NewArticleUrl(start_url):
    # header = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0'}
    web_url = "%s%s" % (start_url, '29278?PAGEN_1=')
    file_craw = open("craw_rosenergoatom.txt", "w")
    file_craw.close()
    count = 7
    global numberArticle

    while (count >= 0):
        page_url = "%s%s" % (web_url, count)
        code = requests.get(page_url)
        plain = code.text
        s = BeautifulSoup(plain, "html.parser")
        count -= 1

        for a in s.findAll('p', {'class':'news-item'}):
            print("NUMBER OF ARTICLE: ", numberArticle, '\n')
            item_id = a.get('id')
            length = len(item_id)
            item_start = item_id.rfind('_', 0, length) + 1
            item = item_id[item_start:length:1] + '/'
            Crawler("%s%s" % (start_url, item))
            numberArticle += 1



def OldArticleUrl(start_url):
    header = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0'}
    web_url = "%s%s" % (start_url, '?PAGEN_1=')
    file_craw = open("craw_rosenergoatom.txt", "a")
    file_craw.close()
    count = 0
    global numberArticle

    # Определение кол-ва страниц
    url_pages = "%s%s" % (web_url, 0)
    code_pages = requestGet(url_pages)
    # code_pages = requests.get(url_pages, headers=header)
    soup_page = BeautifulSoup(code_pages.text, "html.parser")
    pages = soup_page.find('a',{'class':'modern-page-dots'}).find_next_sibling('a')


    while (count <= int(pages.text)):
        page_url = "%s%s" % (web_url, count)
        # code = requests.get(page_url)
        code = requestGet(page_url)
        plain = code.text
        s = BeautifulSoup(plain, "html.parser")
        count += 1
        head = s.findAll('div', {'class':'news-list'})[2]

        for a in head.findAll('p', {'class':'news-item'}):
            print("NUMBER OF ARTICLE: ", numberArticle, '\n')
            item_id = a.get('id')
            length = len(item_id)
            item_start = item_id.rfind('_', 0, length) + 1
            item = 'index.php?ELEMENT_ID=' + item_id[item_start:length:1]
            Crawler("%s%s" % (start_url, item))
            numberArticle += 1



def Crawler(url):
    # header = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0'}
    # code = requests.get(url)
    code = requestGet(url)
    soup = BeautifulSoup(code.text, "html.parser")
    file_craw = open("craw_rosenergoatom.txt", mode='a', encoding='utf8')
    print(url)


    #Дата
    try:
        div = soup.find('div', {'id': 'content'})
        date = div.find('span', {'class': 'news-date-time'})
        dateText = "\n%s %s\n" % ("DATE:", date.text)
    except:
        dateText = "DATE:\n"
    print(dateText)
    file_craw.write(dateText)


    #Tag
    # tag = soup.find('div', {'class':'col-lg-6 content-block'}).find('h1')
    try:
        tag = div.find('small', {'class': 'sourcetext'})
        tagText = "%s %s\n" % ("TAG:", tag.text.strip())
    except:
        tagText = "TAG:\n"
    print(tagText)
    file_craw.write(tagText)


    #Заголовок
    try:
        title = div.find('p', {'class': 'detnewsTitle'})
        titleText = "%s %s\n" % ("TITLE:", title.text.strip())
    except:
        titleText = "TITLE:\n"
    print(titleText)
    file_craw.write(titleText)



    #Статья
    try:
        content = div.find('div').find('div')
        contentText = "%s %s\n" % ("CONTENT:", content.text.strip().replace("\n", ""))
    except:
        contentText = "CONTENT:\n"
    print(contentText)
    file_craw.write(contentText)


    #Разделитель
    separatorText = "______________________________________________________________________________________\n"
    print(separatorText)
    file_craw.write(separatorText)

    file_craw.close()

    # Обращение к внешнему объекту elasticsearchCrawlerClient
    # try:
    #     if elasticsearchCrawlerClient.contains(url) is False:
    #         elasticsearchCrawlerClient.put(url, contentText, dateText, tagText)
    # except Exception:
    #     print('Ошибка записи в базу')



def requestGet(url):
    while True:
        try:
            rs = requests.get(url)
            if rs.status_code != 200:
                print("Ошибка, Код ответа: %s", rs.status)
                time.sleep(30)

                # Попробуем снова на следующей итерации цикла
                continue

            # Если дошли до сюда, значит ошибок не было
            return rs

        except ConnectionError:
            print("Ошибка ConnectionError")
            time.sleep(1)



# Подсчет кол-ва статей
numberArticle = 0

# NewArticleUrl('http://www.rosenergoatom.ru/zhurnalistam/novosti-otrasli/')

year = 2010
while (year <= 2016):
    old_url = 'http://www.rosenergoatom.ru/zhurnalistam/news-archive/'
    year_url = str(year) + '/'
    OldArticleUrl("%s%s" % (old_url, year_url))
    year += 1


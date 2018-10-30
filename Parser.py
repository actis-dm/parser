from proxy_getter import get_viable_proxy_list
from proxy_getter import get_html_proxy
import requests
import time
import random
import os
from bs4 import BeautifulSoup

def get_html(url, useragent, proxy):
	# при выполнении get получаем ответ Response 200. Это означает что все ок.
	r = requests.get(url, timeout = None, headers = useragent, proxies = {'': proxy})
	return r.text

def NewArticleUrl(start_url):
    time.sleep(round(abs(random.gauss(1.5, 1) + random.random() / 10 + random.random() / 100), 4))
    useragent = {'User-Agent': random.choice(list_of_user_agents)}
    proxy = {'http': random.choice(list_of_viable_proxies)}

    web_url = "%s%s" % (start_url, '29278?PAGEN_1=')
    file_craw = open("craw_rosenergoatom.txt", "w")
    file_craw.close()
    count = 7
    global numberArticle

    while (count >= 0):
        page_url = "%s%s" % (web_url, count)
        code = get_html(page_url, useragent, proxy)
        s = BeautifulSoup(code, "html.parser")
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
    time.sleep(round(abs(random.gauss(1.5, 1) + random.random() / 10 + random.random() / 100), 4))
    useragent = {'User-Agent': random.choice(list_of_user_agents)}
    proxy = {'http': random.choice(list_of_viable_proxies)}

    web_url = "%s%s" % (start_url, '?PAGEN_1=')
    file_craw = open("craw_rosenergoatom.txt", "a")
    file_craw.close()
    count = 0
    global numberArticle

    # Определение кол-ва страниц
    url_pages = "%s%s" % (web_url, 0)
    code_pages = get_html(url_pages, useragent, proxy)
    soup_page = BeautifulSoup(code_pages, "html.parser")
    pages = soup_page.find('a',{'class':'modern-page-dots'}).find_next_sibling('a')


    while (count <= int(pages.text)):
        page_url = "%s%s" % (web_url, count)
        code = get_html(page_url, useragent, proxy)
        s = BeautifulSoup(code, "html.parser")
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
    time.sleep(round(abs(random.gauss(1.5, 1) + random.random() / 10 + random.random() / 100), 4))
    useragent = {'User-Agent': random.choice(list_of_user_agents)}
    proxy = {'http': random.choice(list_of_viable_proxies)}


    code = get_html(url, useragent, proxy)
    soup = BeautifulSoup(code, "html.parser")
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



list_of_viable_proxies = get_viable_proxy_list(get_html_proxy('https://www.ip-adress.com/proxy-list'), 10)
cur_dir = os.path.dirname(__file__)
useragent_filename = os.path.join(cur_dir, 'useragents.txt')
list_of_user_agents = open(useragent_filename).read().split('\n')

# Подсчет кол-ва статей
numberArticle = 0

# Статьи за 2017-2018
NewArticleUrl('http://www.rosenergoatom.ru/zhurnalistam/novosti-otrasli/')

# Статьи за 2010-2016
year = 2010
while (year <= 2016):
    old_url = 'http://www.rosenergoatom.ru/zhurnalistam/news-archive/'
    year_url = str(year) + '/'
    OldArticleUrl("%s%s" % (old_url, year_url))
    year += 1


import requests
from bs4 import BeautifulSoup

def NewArticleUrl(start_url):
    header = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0'}
    web_url = "%s%s" % (start_url, '29278?PAGEN_1=')
    file_craw = open("craw_rosenergoatom.txt", "w")
    file_craw.close()
    count = 7

    while (count >= 0):
        page_url = "%s%s" % (web_url, count)
        code = requests.get(page_url, headers=header)
        plain = code.text
        s = BeautifulSoup(plain, "html.parser")
        count -= 1

        for a in s.findAll('p', {'class':'news-item'}):
            item_id = a.get('id')
            item = item_id[13:18:1] + '/'
            Crawler("%s%s" % (start_url, item))



def OldArticleUrl(start_url):
    header = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0'}
    web_url = "%s%s" % (start_url, '?PAGEN_1=')
    file_craw = open("craw_rosenergoatom.txt", "a")
    file_craw.close()
    count = 0

    # Определение кол-ва страниц
    url_pages = "%s%s" % (web_url, 0)
    code_pages = requests.get(url_pages, headers=header)
    soup_page = BeautifulSoup(code_pages.text, "html.parser")
    pages = soup_page.find('a',{'class':'modern-page-dots'}).find_next_sibling('a')


    while (count <= int(pages.text)):
        page_url = "%s%s" % (web_url, count)
        code = requests.get(page_url)
        plain = code.text
        s = BeautifulSoup(plain, "html.parser")
        count += 1
        head = s.findAll('div', {'class':'news-list'})[2]

        for a in head.findAll('p', {'class':'news-item'}):
            item_id = a.get('id')
            item = 'index.php?ELEMENT_ID=' + item_id[14:18:1]
            Crawler("%s%s" % (start_url, item))



def Crawler(url):
    header = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0'}
    code = requests.get(url, headers=header)
    soup = BeautifulSoup(code.text, "html.parser")
    file_craw = open("craw_rosenergoatom.txt", mode='a', encoding='utf8')
    print(url)


    #Дата
    div = soup.find('div', {'id':'content'})
    date = div.find('span', {'class':'news-date-time'})
    if date is None:
        dateText = "DATE:\n"
    else:
        dateText = "\n%s %s\n" % ("DATE:", date.text)
    print(dateText)
    file_craw.write(dateText)


    #Tag
    # tag = soup.find('div', {'class':'col-lg-6 content-block'}).find('h1')
    tag = div.find('small', {'class': 'sourcetext'})
    if tag is None:
        tagText = "TAG:\n"
    else:
        tag = div.find('small', {'class': 'sourcetext'})
        tagText = "%s %s\n" % ("TAG:", tag.text.strip())
    print(tagText)
    file_craw.write(tagText)


    #Заголовок
    title = div.find('p', {'class':'detnewsTitle'})
    if title is None:
        titleText = "TITLE:\n"
    else:
        titleText = "%s %s\n" % ("TITLE:", title.text.strip())
    print(titleText)
    file_craw.write(titleText)



    #Статья
    content = div.find('div').find('div')
    if content is None:
        contentText = "CONTENT:\n"
    else:
        contentText = "%s %s\n" % ("CONTENT:", content.text.strip().replace("\n", ""))
    print(contentText)
    file_craw.write(contentText)


    #Разделитель
    separatorText = "______________________________________________________________________________________\n"
    print(separatorText)
    file_craw.write(separatorText)

    file_craw.close()



NewArticleUrl('http://www.rosenergoatom.ru/zhurnalistam/novosti-otrasli/')
# Для загрузки данных ранее 2016 тут необходимо сделать цикл, но так как и так много данных грузится, решил пока не делать
# OldArticleUrl('http://www.rosenergoatom.ru/zhurnalistam/news-archive/2016/')
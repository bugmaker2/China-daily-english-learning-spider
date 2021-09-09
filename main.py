# Author: Bugmaker
# Date: 2021.9.8
import requests
from bs4 import BeautifulSoup
import re
import pdfkit
import time

headers = {
    'user-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
}

def get_html(urls):
    """
    Get html from url
    Input: urls::url list
    Output: response::html list
    """
    response = []
    for url in urls:
        response.append(requests.get(url=url,headers=headers).text)
    return response

def get_article_html():
    """
    Get the articles' url first from the mainsite's html.
    Then get the html of the articles.
    Input: main_site_html::str
    Output: article_list::str list
    """
    # mainsite html
    mainsite_url = "https://www.chinadaily.com.cn/world"
    mainsite_html = get_html([mainsite_url])[0]
    # article url
    soup = BeautifulSoup(mainsite_html,features="html.parser")
    # url_string = soup.find_all("div",class_="carousel-caption",href=True)
    url_soup = soup.find_all("div",class_="carousel-caption")
    url_string = str(url_soup)
    key = """href.*(www.*html)"""
    url_list = re.findall(key,url_string)
    key = """blank">(.*)</a>"""
    title_list = re.findall(key,url_string)
    # print(title_list)
    # for i in range(0,len(url_list)):
    #     url_list[i] = "http://" + url_list[i]
    # article_html = get_html(url_list)
    # return article_html
    return url_list,title_list

def save_html_as_pdf(url_list,title_list):
    """
    Scan the list and get the html of every url.
    Save the page as pdf into a certain route.
    Input: article_list::str list
    Output: Saved pdfs
    """
    config = pdfkit.configuration(wkhtmltopdf='D:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    for i in range(0,len(url_list)):
        # replace illeagle characters
        pattern=r'[\\/:*?"<>|\r\n]+'
        filename = re.sub(pattern, "_", title_list[i]) 
        filename = time.strftime("%Y-%m-%d",time.localtime())+"-"+title_list[i]+".pdf"
        pdfkit.from_url(url_list[i],filename,configuration=config)
        print(filename)

def main():
    article_url,article_title = get_article_html()
    save_html_as_pdf(article_url,article_title)


if __name__ == "__main__":
    main()

from msilib.schema import Error
import requests
from bs4 import BeautifulSoup as bs
from random import randint
from enum import Enum

URLS = ["https://mgsu.ru/student/Raspisanie_zanyatii_i_ekzamenov/fayly-raspisaniya-dlya-skachivaniya/",
        "https://www.architect4u.ru/articles.html", "https://www.architect4u.ru/articles-2.html",
        "https://www.architect4u.ru/articles-3.html"]

def check_status(self):
    if str(self.__r.status_code)[0] == '5':
        return "Ошибка сервера!"

    elif str(self.__r.status_code) == '404':
        return "Страница не найдена!"

    return "Нет информации, возможно на сайте технические работы"


class MGSUParser:
    def __init__(self):
        self.__r = requests.get(URLS[0], verify=False)
        self.__soup = bs(self.__r.text, "html.parser")
        self.__week = self.__soup.find_all('h4')

    async def set_week(self):
        if self.__r.status_code == 200:
            for self.data in self.__week:
                if (self.data.find('b') is not None) and ("неделя" in str(self.data.text)):
                    return self.data.text

        else:
            check_status(self)


class ArticlesParser:
    def __init__(self):
        self.__r = requests.get(URLS.pop(randint(1, len(URLS) - 1)))
        self.__soup = bs(self.__r.text, "html.parser")
        self.__articles = self.__soup.findAll("div", class_="card")

    async def get_random_article(self):
        if self.__r.status_code == 200:
            articles_hrefs = []
            for article in self.__articles:
                articles_hrefs.append(article.a['href'])
            return "https://www.architect4u.ru/" + articles_hrefs.pop(randint(0, len(articles_hrefs) - 1))

        else:
            check_status(self)


class ParserFactory:
    def create_parser_instance(parser_type):
        if (parser_type == "MGSU"):
            return MGSUParser()
        elif (parser_type == "ARTICLE"):
            return ArticlesParser()
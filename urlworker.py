import requests
from bs4 import BeautifulSoup as bs
from random import randint

URLS = ["https://mgsu.ru/student/Raspisanie_zanyatii_i_ekzamenov/fayly-raspisaniya-dlya-skachivaniya/",
        "https://www.architect4u.ru/articles.html", "https://www.architect4u.ru/articles-2.html",
        "https://www.architect4u.ru/articles-3.html"]


class MGSUParser:
    def __init__(self, url = URLS[0]):
        self.r = requests.get(url, verify=False)
        self.soup = bs(self.r.text, "html.parser")
        self.week = self.soup.find_all('h4')

    def check_status(self):
        if str(self.r.status_code)[0] == '5':
            return "Ошибка сервера!"

        elif str(self.r.status_code) == '404':
            return "Страница не найдена!"

        return "Нет информации, возможно, на сайте ведутся технические работы"

    def set_week(self):
        if self.r.status_code == 200:
            for data in self.week:
                if (data.find('b') is not None) and ("неделя" in str(data.text)):
                    return data.text

        else:
            self.check_status()


class ArticlesParser(MGSUParser):
    def __init__(self):
        super().__init__(url = URLS.pop(randint(1, len(URLS) - 1)))
        self.articles = self.soup.findAll("div", class_="card")

    def get_random_article(self):
        if self.r.status_code == 200:
            articles_hrefs = []
            for article in self.articles:
                articles_hrefs.append(article.a['href'])
            return "https://www.architect4u.ru/" + articles_hrefs.pop(randint(0, len(articles_hrefs) - 1))

        else:
            self.check_status()


class ParserFactory:
    @staticmethod
    def create_mgsu_parser():
        return MGSUParser()

    @staticmethod
    def create_articles_parser():
        return ArticlesParser()

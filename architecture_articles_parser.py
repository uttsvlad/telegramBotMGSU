from random import randint
import requests
from bs4 import BeautifulSoup as bs

ARCHITECT4U_URLS = ["https://www.architect4u.ru/articles.html", "https://www.architect4u.ru/articles-2.html",
                    "https://www.architect4u.ru/articles-3.html"]


def get_random_article_from_architect4u():
    global response
    try:
        response = requests.get(ARCHITECT4U_URLS.pop(randint(0, len(ARCHITECT4U_URLS) - 1)))
    except ConnectionError:
        status_code = response.status_code
        if status_code >= 400 & status_code <= 417:
            return "Упс, непредвиденная ошибка в работе"
        elif status_code >= 500 & status_code <= 505:
            return "Упс, непредвиденная ошибка на сервере"
        elif response.status_code != 200:
            return "Упс, ничего не найдено"

    soup = bs(response.text, "html.parser")
    articles = soup.findAll("div", class_="card")
    articles_hrefs = []
    for article in articles:
        articles_hrefs.append(article.a['href'])
    return "https://www.architect4u.ru/" + articles_hrefs.pop(randint(0, len(articles_hrefs) - 1))

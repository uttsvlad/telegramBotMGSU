import re

import res

import requests
from bs4 import BeautifulSoup as Bs
from random import randint


class MGSUParser:
    def __init__(self, url=res.MGSU_URLS[0]):
        self.r = requests.get(url, verify=False)
        self.soup = Bs(self.r.text, "html.parser")
        self.directions_result_dict = {}

    def check_status(self):
        if str(self.r.status_code)[0] == "5":
            return res.SERVER_ERROR

        elif str(self.r.status_code) == "404":
            return res.PAGE_NOT_FOUND

        return res.NO_INFO_ABOUT_PAGE

    def get_week(self):
        if self.r.url != res.MGSU_URLS[0]:
            self.r = requests.get(res.MGSU_URLS[0], verify=False)
            self.soup = Bs(self.r.text, "html.parser")
        if self.r.status_code == 200:
            week = self.soup.find_all("h4")
            for data in week:
                if (data.find("b") is not None) and ("неделя" in str(data.text)):
                    return data.text

        else:
            self.check_status()

    def get_door_opened__day(self):
        if self.r.url != res.MGSU_URLS[1]:
            self.r = requests.get(res.MGSU_URLS[1], verify=False)
            self.soup = Bs(self.r.text, "html.parser")
        if self.r.status_code == 200:
            date = self.soup.find("div", {"id": "content"}).find("div", {"id": "inner-content"}).findAll("span")
            result_data = []
            for data in date:
                if "для поступающих" in str(data.text):
                    result_data.append(data.text.replace("\xa0", ""))
            return result_data

        else:
            self.check_status()

    def get_door_opened_day_reg_url(self):
        if self.r.url != res.MGSU_URLS[1]:
            self.r = requests.get(res.MGSU_URLS[1], verify=False)
            self.soup = Bs(self.r.text, "html.parser")
        if self.r.status_code == 200:
            return self.soup.find("div", {"id": "content"}).find("div", {"id": "inner-content"}).find("a").attrs[
                "href"]
        else:
            self.check_status()

    def get_directions(self, answer):
        self.directions_result_dict = {}
        if answer.startswith("bac"):
            if self.r.url != res.MGSU_URLS[2]:
                self.r = requests.get(res.MGSU_URLS[2], verify=False)
                self.soup = Bs(self.r.text, "html.parser")
        elif answer.startswith("mag"):
            if self.r.url != res.MGSU_URLS[3]:
                self.r = requests.get(res.MGSU_URLS[3], verify=False)
                self.soup = Bs(self.r.text, "html.parser")
        elif answer == "asp":
            return self.get_info_about_direction("asp")

        if self.r.status_code == 200:
            directions = self.soup.find("div", {
                "class": "col-lg-8 col-md-8 col-sm-8 col-xs-12"}).findAll("ul")
            result_directions = []
            if answer.endswith("_och"):
                result_directions = directions[0].findAll("li")
            elif answer.endswith("_och_zaoch") or answer.endswith("mag_zaoch"):
                result_directions = directions[1].findAll("li")
            elif answer.endswith("_zaoch"):
                result_directions = directions[2].findAll("li")

            for direction in result_directions:
                direction_url = direction.a["href"]
                if not direction_url.startswith("http://mgsu.ru/") and not direction_url.startswith(
                        "https://mgsu.ru/"):
                    direction_url = "https://mgsu.ru/" + direction.a["href"]
                self.directions_result_dict[direction.text.strip()] = direction_url
            return self.directions_result_dict
        else:
            self.check_status()

    def get_info_about_direction(self, direction_name):
        if direction_name == "asp":
            if self.r.url != res.MGSU_URLS[4]:
                self.r = requests.get(res.MGSU_URLS[4], verify=False)
                self.soup = Bs(self.r.text, "html.parser")
            if self.r.status_code == 200:
                direction_info = []
                info = self.soup.find("table", {"class": "MsoNormalTable"}).findAll("tr")
                for i in info:
                    direction_info.append(i.text)
                direction_info.pop(0)
                direction_info_buf = []
                for i in direction_info:
                    direction_info_buf.append(i.replace("\n", "").strip())
                result_info = ""
                for td in direction_info_buf:
                    buf = td.split(" ")
                    buf.insert(len(buf) - 2, res.FREE_STUDYING_COUNT)
                    buf.insert(len(buf) - 1, res.PAID_STUDYING_COUNT)
                    buf.insert(len(buf), res.DELIMITER)
                    result_info += " ".join(buf)
                return result_info
            else:
                self.check_status()

        elif self.r.url != self.directions_result_dict[direction_name]:
            self.r = requests.get(self.directions_result_dict[direction_name], verify=False)
            self.soup = Bs(self.r.text, "html.parser")
            if direction_name == res.VERY_BAD_PAGE_NAME:
                return self.directions_result_dict[res.VERY_BAD_PAGE_NAME]
            if self.r.status_code == 200:
                direction_info = ""
                info_names = []
                info = self.soup.find("div",
                                      {"class": "col-lg-8 col-md-8 col-sm-8 col-xs-12"}).findAll("td",
                                                                                                 {"bgcolor": "#0a4d83"})
                for name in info:
                    info_names.append(
                        re.sub(" +", " ", name.text.replace("\n", "").replace("*", "").replace("\xa0", "").strip()))
                if res.BAD_FORM_NAME in info_names:
                    info_names.remove(res.BAD_FORM_NAME)
                info_values = []
                info = self.soup.find("div",
                                      {"class": "col-lg-8 col-md-8 col-sm-8 col-xs-12"}).findAll("td",
                                                                                                 {"bgcolor": "#d7d7d7"})
                for value in info:
                    info_values.append(value.text.replace("\n", "").replace("*", "").replace("\xa0", "").strip())
                info_values.pop(0)
                if res.BAD_FORM_1 in info_values:
                    info_values.remove(res.BAD_FORM_1)
                elif res.BAD_FORM_2 in info_values:
                    info_values.remove(res.BAD_FORM_2)
                elif res.BAD_FORM_3 in info_values:
                    info_values.remove(res.BAD_FORM_3)

                if res.FREE not in info_names:
                    info_names.insert(0, res.PAID_STUDYING)
                    info_values.insert(0, "")
                    info_names.insert(4, res.ADDITIONAL_INFO_EMOJI)
                    info_values.insert(4, "")
                else:
                    info_names.insert(0, res.FREE_STUDYING)
                    info_values.insert(0, "")

                    for i in [2, 4, 5]:
                        if info_names[1] == info_names[i]:
                            info_names.insert(i, res.PAID_STUDYING)
                            info_values.insert(i, "")
                            info_names.insert(2 * i, res.ADDITIONAL_INFO_EMOJI)
                            info_values.insert(2 * i, "")
                            break

                info_values.reverse()

                for name in info_names:
                    direction_info += name + ": " + info_values.pop() + "\n\n"
                return direction_info
            else:
                self.check_status()

    def get_students_houses_with_img(self):
        if self.r.url != res.MGSU_URLS[5]:
            self.r = requests.get(res.MGSU_URLS[5], verify=False)
            self.soup = Bs(self.r.text, "html.parser")
        if self.r.status_code == 200:
            students_houses_info = []  # 0 - text, 1 - img
            founded = self.soup.find("div", {"class": "col-lg-8 col-md-8 col-sm-8 col-xs-12"})
            students_houses_info.append(founded.text.replace("\n", ""))
            students_houses_info.append(founded.find("img")["src"])
            return students_houses_info
        else:
            self.check_status()


class ArticlesParser(MGSUParser):
    def __init__(self):
        super().__init__(url=res.ARTICLE_URLS.pop(randint(1, len(res.ARTICLE_URLS) - 1)))
        self.articles = self.soup.findAll("div", class_="card")

    def get_random_article(self):
        if self.r.status_code == 200:
            articles_hrefs = []
            for article in self.articles:
                articles_hrefs.append(article.a["href"])
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

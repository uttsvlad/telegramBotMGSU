import re

import requests
from bs4 import BeautifulSoup as Bs
from random import randint
import os
from workers import fileworker
from res import res

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
        if not (os.path.isfile("houses.txt")):
            if self.r.url != res.MGSU_URLS[1]:
                self.r = requests.get(res.MGSU_URLS[1], verify=False)
                self.soup = Bs(self.r.text, "html.parser")
            if self.r.status_code == 200:
                date = self.soup.find("div", {"id": "content"}).find("div", {"id": "inner-content"}).findAll("span")
                result_data = []
                for data in date:
                    if "для поступающих" in str(data.text):
                        result_data.append(data.text.replace("\xa0", ""))
                fileworker.write_to_file("open_day.txt", "~".join(result_data) + "~", "w")
                return result_data

            else:
                self.check_status()
        else:
            answer = fileworker.read_from_file("open_day.txt").split("~")
            return answer[:len(answer) - 1]

    def get_door_opened_day_reg_url(self):
        if not (os.path.isfile("houses.txt")):
            if self.r.url != res.MGSU_URLS[1]:
                self.r = requests.get(res.MGSU_URLS[1], verify=False)
                self.soup = Bs(self.r.text, "html.parser")
            if self.r.status_code == 200:
                answer = self.soup.find("div", {"id": "content"}).find("div", {"id": "inner-content"}).find("a").attrs[
                    "href"]
                fileworker.write_to_file("open_day.txt", str(answer), "a")
                return answer
            else:
                self.check_status()
        else:
            return fileworker.read_from_file("open_day.txt").split("~")[-1]

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
                if not direction_url.startswith(res.HTTP_MGSU) and not direction_url.startswith(
                        res.HTTPS_MGSU):
                    direction_url = res.HTTPS_MGSU + direction.a["href"]
                self.directions_result_dict[direction.text.strip()] = direction_url
            return self.directions_result_dict
        else:
            self.check_status()

    def get_info_about_direction(self, direction_name):

        if direction_name == "asp" and not (os.path.isfile("asps.txt")):
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
                fileworker.write_to_file("asps.txt", result_info, "w")
                return result_info  # засунуть в текстовый файл
            else:
                self.check_status()
        elif (direction_name == "asp") and os.path.isfile("asps.txt"):
            return fileworker.read_from_file("asps.txt")

        elif self.r.url != self.directions_result_dict[direction_name] and not (
                os.path.isfile(direction_name + ".txt")):
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
                direction_info += res.MORE + ":\n" + self.directions_result_dict[direction_name]
                fileworker.write_to_file(direction_name + ".txt", direction_info, "w")
                return direction_info
            else:
                self.check_status()
        elif self.r.url != self.directions_result_dict[direction_name] and os.path.isfile(direction_name + ".txt"):
            return fileworker.read_from_file(direction_name + ".txt")

    def get_students_houses_with_img(self):
        if not (os.path.isfile("houses.txt")):
            if self.r.url != res.MGSU_URLS[5]:
                self.r = requests.get(res.MGSU_URLS[5], verify=False)
                self.soup = Bs(self.r.text, "html.parser")
            if self.r.status_code == 200:
                students_houses_info = []  # 0 - img, 1 - txt
                founded = self.soup.find("div", {"class": "col-lg-8 col-md-8 col-sm-8 col-xs-12"})
                students_houses_info.append(founded.find("img")["src"])
                students_houses_info.append(founded.text.replace("\n", ""))

                fileworker.write_to_file("houses.txt", "~".join(students_houses_info), "w")
                return students_houses_info
            else:
                self.check_status()
        else:
            return fileworker.read_from_file("houses.txt").split("~")

    def get_olympics(self):
        if not (os.path.isfile("olympics.json")):
            if self.r.url != res.MGSU_URLS[6]:
                self.r = requests.get(res.MGSU_URLS[6], verify=False)
                self.soup = Bs(self.r.text, "html.parser")
            if self.r.status_code == 200:
                result = {}
                info = self.soup.find("div", {"class": "col-lg-8 col-md-8 col-sm-8 col-xs-12"}).find("ul").findAll("li")
                for i in info:
                    result[i.text] = i.a["href"]
                result[res.MORE] = res.OLYMPICS_MORE
                fileworker.write_to_json("olympics.json", result)
                return result
            else:
                self.check_status()
        else:
            return fileworker.read_from_json("olympics.json")

    def get_architect_course(self):
        if not (os.path.isfile("architect.json")):
            if self.r.url != res.MGSU_URLS[7]:
                self.r = requests.get(res.MGSU_URLS[7], verify=False)
                self.soup = Bs(self.r.text, "html.parser")
            if self.r.status_code == 200:
                urls = {}
                image = self.soup.find("div", {"class": "col-lg-8 col-md-8 col-sm-8 col-xs-12"}).find("img")
                if not image["src"].startswith(res.HTTP_MGSU) and not image["src"].startswith(
                        res.HTTPS_MGSU):
                    urls["image"] = (res.HTTPS_MGSU + image["src"])
                info = self.soup.find("div", {"class": "col-lg-8 col-md-8 col-sm-8 col-xs-12"}).findAll("a")
                for i in info:
                    url = i["href"]
                    if not url.startswith(res.HTTP_MGSU) and not url.startswith(
                            res.HTTPS_MGSU) and "youtube" not in url:
                        urls[i.text.replace("\n", "").strip()] = (res.HTTPS_MGSU + url)
                    else:
                        urls[i.text.replace("\n", "").strip()] = url
                urls[res.MORE] = self.r.url
                text = self.soup.find("div", {"class": "col-lg-8 col-md-8 col-sm-8 col-xs-12"}).find("p")
                urls["text"] = text.text.replace("\n", "").strip()
                urls.pop("")
                fileworker.write_to_json("architect.json", urls)
                return urls
            else:
                self.check_status()
        else:
            return fileworker.read_from_json("architect.json")

    def get_ege_courses(self):
        if not (os.path.isfile("ege.json")):
            if self.r.url != res.MGSU_URLS[8]:
                self.r = requests.get(res.MGSU_URLS[8], verify=False)
                self.soup = Bs(self.r.text, "html.parser")
            if self.r.status_code == 200:
                result = {}
                info = self.soup.find("div", {"class": "col-lg-8 col-md-8 col-sm-8 col-xs-12"}).findAll("td")
                result["text"] = info[2].text
                for i in range(3, 10):
                    url = info[i].a["href"]
                    if not url.startswith(res.HTTP_MGSU) and not url.startswith(
                            res.HTTPS_MGSU):
                        result[info[i].text.replace("\n", "").strip()] = (res.HTTPS_MGSU + url)
                    else:
                        result[info[i].text.replace("\n", "").strip()] = info[i].a["href"]

                result[res.MORE] = res.EGE_COURSES_MORE
                fileworker.write_to_json("ege.json", result)
                return result
            else:
                self.check_status()
        else:
            return fileworker.read_from_json("ege.json")


class ArticlesParser(MGSUParser):
    def __init__(self):
        super().__init__(url=res.ARTICLE_URLS.pop(randint(1, len(res.ARTICLE_URLS) - 1)))
        self.articles = self.soup.findAll("div", class_="card")

    def get_random_article(self):
        if self.r.status_code == 200:
            articles_hrefs = []
            for article in self.articles:
                articles_hrefs.append(article.a["href"])
            return res.ARCH_4_U + articles_hrefs.pop(randint(0, len(articles_hrefs) - 1))

        else:
            self.check_status()


class ParserFactory:
    @staticmethod
    def create_mgsu_parser():
        return MGSUParser()

    @staticmethod
    def create_articles_parser():
        return ArticlesParser()

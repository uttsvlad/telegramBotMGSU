from cgi import test
import unittest
import requests as r
from workers import urlworker
import main
import re
from workers import fileworker
import os
import res

class TestMGSUParser(unittest.TestCase):
    @unittest.skipIf(r.get("https://google.com").status_code != 200, "It seems that there is no Internet!")
    def test_connection(self):
        test_obj = urlworker.MGSUParser()
        self.assertEqual(200, test_obj.r.status_code)

    @unittest.skipIf(r.get("https://google.com").status_code != 200, "It seems that there is no Internet!")
    def test_status_code(self):
        test_obj = urlworker.MGSUParser(url="https://mgsu.ru/abrakadabra")
        self.assertEqual("Страница не найдена!", test_obj.check_status())

class TestMain(unittest.TestCase):
    def test_markup(self):
        self.assertTrue(re.match(r'Ближайший день открытых дверей?', main.get_default_markup().keyboard[0][0]['text']))
        self.assertTrue(re.match(r'Олимпиады?', main.get_default_markup().keyboard[1][0]['text']))
        self.assertTrue(re.match(r'Направления обучения?', main.get_default_markup().keyboard[2][0]['text']))
        self.assertTrue(re.match(r'Курсы подготовки?', main.get_default_markup().keyboard[3][0]['text']))
        self.assertTrue(re.match(r'Общежития?', main.get_default_markup().keyboard[4][0]['text']))
        self.assertTrue(re.match(r'Дополнительная информация?', main.get_default_markup().keyboard[5][0]['text']))
        self.assertTrue(re.match(r'Статья об архитектуре?', main.get_default_markup().keyboard[6][0]['text']))
        
class TestLinks(unittest.TestCase):
    @unittest.skipIf(r.get("https://google.com").status_code != 200, "It seems that there is no Internet!")
    def test_is_valid_olympics(self):
        test_obj = urlworker.MGSUParser()
        olympics = test_obj.get_olympics()
        for i in olympics:
            self.assertTrue(r.get(str(olympics[i]), verify=False).status_code == 200)

    @unittest.skipIf(r.get("https://google.com").status_code != 200, "It seems that there is no Internet!")
    def test_is_valid_house(self):
        test_object = urlworker.MGSUParser()
        self.assertTrue(r.get(test_object.get_students_houses_with_img()[0], verify=False).status_code == 200)

    @unittest.skipIf(r.get("https://google.com").status_code != 200, "It seems that there is no Internet!")
    def test_is_valid_open_day(self):
        test_object = urlworker.MGSUParser()
        self.assertTrue(r.get(test_object.get_door_opened_day_reg_url().split("~")[-1], verify=False).status_code == 200)

    
class TestArticlesParser(unittest.TestCase):
    @unittest.skipIf(r.get("https://google.com").status_code != 200, "It seems that there is no Internet!")
    def test_is_valid_article(self):
        test_object = urlworker.ArticlesParser()
        for i in range(0, 3):
            self.assertTrue(r.get(test_object.get_random_article(), verify=False).status_code == 200)
    
    @unittest.skipIf(r.get("https://google.com").status_code != 200, "It seems that there is no Internet!")
    def test_is_random_article(self):
        test_object = urlworker.ArticlesParser()
        self.assertNotEqual(test_object.get_random_article(), test_object.get_random_article())

class TestFileWorker(unittest.TestCase):
    def test_writing_to_txt(self):
        if os.path.isfile("res/test.txt"):
            os.remove("res/test.txt")
            fileworker.write_to_file("test.txt", "This is a test string writed to test file by test.py", "w")
            self.assertTrue(os.path.isfile("res/test.txt"))
        else:
            fileworker.write_to_file("test.txt", "This is a test string writed to test file by test.py", "w")
            self.assertTrue(os.path.isfile("res/test.txt"))

    def test_writing_to_json(self):
        if os.path.isfile("res/test.json"):
            os.remove("res/test.json")
            fileworker.write_to_json("test.json", {"test":"this is test json"})
            self.assertTrue(os.path.isfile("res/test.json"))
        else:
            fileworker.write_to_json("test.json", {"test":"this is test json"})
            self.assertTrue(os.path.isfile("res/test.json"))

    @unittest.skipIf(not os.path.isfile("res/test.txt"), "File is not exist!")
    def test_reading_from_txt(self):
        test_text = fileworker.read_from_file("test.txt")
        os.remove("res/test.txt")
        self.assertEqual(test_text, "This is a test string writed to test file by test.py")

    @unittest.skipIf(not os.path.isfile("res/test.json"), "File is not exist!")
    def test_reading_from_json(self):
        test_text = fileworker.read_from_json("test.json")
        os.remove("res/test.json")
        self.assertEqual(test_text["test"], "this is test json")

class TestWeek(unittest.TestCase):
    def week_tester(self):
        test_obj = urlworker.MGSUParser()
        self.assertEqual(test_obj.get_week(), r'Сейчас идёт*')

if __name__ == '__main__':
    unittest.main()
    
    
from msilib.schema import Error
import requests
from bs4 import BeautifulSoup as bs

class Parser():
    def __init__(self, url):
    
        self.__r = requests.get(url, verify=False)    
        self.__soup = bs(self.__r.text, "html.parser")
        self.__week = self.__soup.find_all('h4')

    def set_week(self):

        if self.__r.status_code == 200:
            for self.data in self.__week:
                if (self.data.find('b') is not None) and ("неделя" in str(self.data.text)):
                    return self.data.text
            return "Нет информации, возможно на сайте технические работы"

        elif str(self.__r.status_code)[0] == '5':
            return "Server Error!"

        elif str(self.__r.status_code) == '404':
            return "Page not found!"
        
        
        
            
p = Parser("https://mgsu.ru/student/Raspisanie_zanyatii_i_ekzamenov/fayly-raspisaniya-dlya-skachivaniya/")

print(p.set_week())

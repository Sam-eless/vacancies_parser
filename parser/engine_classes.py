from parser.classes import SJVacancy
import requests
import json
import os

from abc import ABC, abstractmethod
from pprint import pprint




class Engine(ABC):
    @abstractmethod
    def get_request(self):
        pass

    @staticmethod
    def get_connector(file_name):
        """ Возвращает экземпляр класса Connector """
        pass


class HH(Engine):
    """Метод делает запрос к API hh.ru и создает объекты"""

    def __init__(self, word: str, page=1, town='Moscow'):
        self.word = word
        self.page = page
        self.town = town
        data = self.get_request()
        pprint(data)
        self.name = data['items'][0]['name']
        self.url_link = data['items'][0]['apply_alternate_url']
        self.description = data['items'][0]['snippet']['responsibility']
        try:
            self.salary_from = data['items'][0]['salary']['from']
            self.salary_to = data['items'][0]['salary']['to']
        except TypeError:
            self.salary = None


    def get_request(self):
        response = requests.get(f'https://api.hh.ru/vacancies?text={self.word}&per_page=1&page=0&area=1')
        data = response.json()
        return data


class SuperJob(Engine):
    def __init__(self, word: str, page=1, town='Moscow'):

        self.word = word
        self.page = page
        self.town = town
        data = self.get_request()
        for i in range(20):
            try:
                # pprint(data)
                try:
                    self.name = data['objects'][i]['profession']
                except NameError:
                    self.name = None
                self.url_link = data['objects'][i]['link']
                try:
                    self.description = data['objects'][i]['client']['description']
                except:
                    self.description = None
                self.salary = data['objects'][i]['payment_from'], data['objects'][i]['payment_to']
                SJVacancy.all_vacancies.append(SJVacancy(self.name, self.url_link, self.description, self.salary))
            except IndexError:
                print("Больше вакансий не найдено.")


    def get_request(self):
        my_auth_data = {'X-Api-App-Id': os.environ['SUPERJOB_API_KEY']}
        response = requests.get('https://api.superjob.ru/2.0/vacancies/', headers=my_auth_data, params={'keywords': {self.word}, 'page':{self.page},  'count':20, 'town':{self.town}})
        data = response.json()
        return data


hh = HH('python')
# for i in range(1):
#     sj = SuperJob("python", i, 'Москва')
#
# for i in SJVacancy.all_vacancies:
#        print(i)
#
# print((SJVacancy.get_count_of_vacancy))

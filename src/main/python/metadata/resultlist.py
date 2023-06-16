import json
import re
import urllib

import requests
from bs4 import BeautifulSoup
from constants import REQUEST_TIME_OUT


class ResultList:
    def __init__(self, province, city) -> None:
        self.province = province
        self.city = city

    def get_result_list(self, curl):
        func_name = f"result_list_{str(self.province)}_{str(self.city)}"
        func = getattr(self, func_name, self.result_list_other)
        return func(curl)

    def result_list_sichuan_sichuan(self, curl):
        response = requests.get(curl['url'], params=curl['queries'], headers=curl['headers'], timeout=REQUEST_TIME_OUT)
        html = response.content.decode('utf-8')
        soup = BeautifulSoup(html, "html.parser")
        # soup = BeautifulSoup(html, "lxml")
        links = []

        for dataset in soup.find('div', attrs={'class': 'bottom-content'}).find('ul').find_all('li', recursive=False):
            link = dataset.find('div', attrs={
                'class': 'cata-title'
            }).find('a', attrs={'href': re.compile("/oportal/catalog/*")})
            data_formats = []
            for data_format in dataset.find('div', attrs={'class': 'file-type'}).find_all('li'):
                data_format_text = data_format.get_text()
                if data_format_text == '接口':
                    data_format_text = 'api'
                data_formats.append(data_format_text.lower())
            links.append({'link': link['href'], 'data_formats': str(data_formats)})
        return links

    def result_list_sichuan_chengdu(self, curl):
        response = requests.get(curl['url'], params=curl['queries'], headers=curl['headers'], timeout=REQUEST_TIME_OUT)
        html = response.content.decode('utf-8')
        soup = BeautifulSoup(html, "html.parser")
        # soup = BeautifulSoup(html, "lxml")
        links = []

        for dataset in soup.find('div', attrs={'class': 'bottom-content'}).find('ul').find_all('li', recursive=False):
            link = dataset.find('div', attrs={
                'class': 'cata-title'
            }).find('a', attrs={'href': re.compile("/oportal/catalog/*")})
            data_formats = []
            for data_format in dataset.find('div', attrs={'class': 'file-type'}).find_all('li'):
                data_format_text = data_format.get_text()
                if data_format_text == '接口':
                    data_format_text = 'api'
                data_formats.append(data_format_text.lower())
            links.append({'link': link['href'], 'data_formats': str(data_formats)})
        return links


    def result_list_sichuan_zigong(self, curl):
        response = requests.get(curl['url'], params=curl['queries'], headers=curl['headers'], timeout=REQUEST_TIME_OUT)

        print(response)
        resultList = json.loads(response.text)['data']['rows']
        ids = [x['id'] for x in resultList]
        return ids

    def result_list_other(self):
        print("暂无该省")
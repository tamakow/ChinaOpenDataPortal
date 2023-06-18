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

    def result_list_sichuan_panzhihua(self, curl):
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

        # print(response)
        resultList = json.loads(response.text)['data']['rows']
        ids = [x['id'] for x in resultList]
        return ids

    def result_list_sichuan_luzhou(self, curl):
        response = requests.post(curl['url'], json=curl['data'], headers=curl['headers'], timeout=REQUEST_TIME_OUT)

        # print(response)
        resultList = json.loads(response.text)['result']['rows']
        ids = [(x['id'], x['openType'], x['publishTime'], x['updateTime']) for x in resultList]
        return ids

    def result_list_sichuan_deyang(self, curl):
        response = requests.post(curl['url'], json=curl['data'], headers=curl['headers'], timeout=REQUEST_TIME_OUT)


        # print(response)
        resultList = json.loads(response.text)['data']['rows']
        ids = [x['mlbh'] for x in resultList]
        return ids

    def result_list_sichuan_mianyang(self, curl):
        response = requests.get(curl['url'], params=curl['queries'], headers=curl['headers'], timeout=REQUEST_TIME_OUT)


        # print(response)
        resultList = json.loads(response.text)['elementthing']['listPage']['list']
        ids = [x['id'] for x in resultList]
        return ids

    def result_list_sichuan_guangyuan(self, curl):
        response = requests.post(curl['url'], json=curl['data'], headers=curl['headers'], timeout=REQUEST_TIME_OUT)

        if response.status_code != requests.codes.ok:
            print("error " + str(response.status_code) + ": " + curl['url'])
            return dict()
        # print(response)
        resultList = json.loads(response.text)['data']['rows']
        ids = [x['ID'] for x in resultList]
        return ids

    def result_list_sichuan_suining(self, curl):
        response = requests.post(curl['url'], json=curl['data'], headers=curl['headers'], timeout=REQUEST_TIME_OUT)

        if response.status_code != requests.codes.ok:
            print("error " + str(response.status_code) + ": " + curl['url'])
            return dict()
        # print(response)
        resultList = json.loads(response.text)['data']['rows']
        ids = [(x['mlbh'], x['wjlx']) for x in resultList]
        return ids

    def result_list_sichuan_neijiang(self, curl):
        response = requests.post(curl['url'], params=curl['queries'], json=curl['data'], headers=curl['headers'], timeout=REQUEST_TIME_OUT)

        if response.status_code != requests.codes.ok:
            print("error " + str(response.status_code) + ": " + curl['url'])
            return dict()
        # print(response)
        resultList = json.loads(response.text)['data']['content']
        ids = [str(x['id']) for x in resultList]
        return ids

    def result_list_sichuan_leshan(self, curl):
        response = requests.get(curl['url'], params=curl['queries'], headers=curl['headers'], timeout=REQUEST_TIME_OUT)

        if response.status_code != requests.codes.ok:
            print("error " + str(response.status_code) + ": " + curl['url'])
            return dict()
        # print(response)
        resultList = json.loads(response.text)['data']['rows']
        ids = [str(x['resourceId']) for x in resultList]
        return ids

    def result_list_sichuan_nanchong(self, curl):
        response = requests.get(curl['url'], params=curl['queries'], headers=curl['headers'], timeout=REQUEST_TIME_OUT)

        if response.status_code != requests.codes.ok:
            print("error " + str(response.status_code) + ": " + curl['url'])
            return dict()
        # print(response)
        resultList = json.loads(response.text)['data']
        ids = [str(x['ID']) for x in resultList]
        return ids

    def result_list_shaanxi_shaanxi(self, curl):
        response = requests.get(curl['url'], params=curl['queries'], headers=curl['headers'], timeout=REQUEST_TIME_OUT)

        if response.status_code != requests.codes.ok:
            print("error " + str(response.status_code) + ": " + curl['url'])
            return dict()
        # print(response)
        resultList = json.loads(response.text)[0]['result']

        metadata_list = []

        for result in resultList:
            dataset_metadata = {}

            dataset_metadata["标题"] = result['sdataName']
            dataset_metadata["来源部门"] = result['sorgName']
            dataset_metadata["所属主题"] = result['sdataTopic']
            dataset_metadata["发布时间"] = result['spubDate'].split(' ')[0].strip()
            dataset_metadata["更新时间"] = result['spubDate'].split(' ')[0].strip()
            dataset_metadata["标签"] = result['keywords'] if 'keyword' in result else ""
            dataset_metadata["描述"] = result['sdataIntro']
            dataset_metadata["数据格式"] = result['sdataFormats']
            dataset_metadata["详情页网址"] = "http://www.sndata.gov.cn/info?id=" + result['id']

            metadata_list.append(dataset_metadata)
        return metadata_list


    def result_list_ningxia_ningxia(self, curl):
        response = requests.get(curl['url'], params=curl['queries'], headers=curl['headers'], timeout=REQUEST_TIME_OUT, verify=False)
        html = response.content.decode('utf-8')
        soup = BeautifulSoup(html, "html.parser")
        # soup = BeautifulSoup(html, "lxml")
        links = []

        for dataset in soup.find('div', attrs={'class': 'bottom-content'}).find('ul').find_all('li', recursive=False):
            link = dataset.find('div', attrs={
                'class': 'cata-title'
            }).find('a', attrs={'href': re.compile("/portal/catalog/*")})
            data_formats = []
            for data_format in dataset.find('div', attrs={'class': 'file-type'}).find_all('li'):
                data_format_text = data_format.get_text()
                if data_format_text == '接口':
                    data_format_text = 'api'
                if data_format_text == '链接':
                    data_format_text = 'link'
                data_formats.append(data_format_text.lower())
            links.append({'link': link['href'], 'data_formats': str(data_formats)})
        return links

    def result_list_xinjiang_wlmq(self, curl):
        response = requests.post(curl['url'], params=curl['queries'], data=curl['data'], headers=curl['headers'], timeout=REQUEST_TIME_OUT)

        if response.status_code != requests.codes.ok:
            print("error " + str(response.status_code) + ": " + curl['url'])
            return dict()
        # print(response)
        resultList = json.loads(response.text)['data']
        ids = [(str(x['cata_id']), x['conf_catalog_format']) for x in resultList]
        return ids

    def result_list_other(self):
        print("暂无该省")
import json
import re
import urllib

import requests
from bs4 import BeautifulSoup
from constants import REQUEST_TIME_OUT


class ResultList:
    def __init__(self, province) -> None:
        self.province = province

    def get_result_list(self, curl):
        func_name = "result_list_" + str(self.province)
        func = getattr(self, func_name, self.result_list_other)
        return func(curl)

    def result_list_beijing(self, curl):
        response = requests.post(curl['url'], data=curl['data'], headers=curl['headers'], timeout=REQUEST_TIME_OUT)
        resultList = json.loads(response.text)['object']['docs']
        print(resultList)
        links = [x['url'] for x in resultList]
        return links

    def result_list_tianjin(self, curl):
        response = requests.get(curl['url'], timeout=REQUEST_TIME_OUT)
        resultList = json.loads(response.text)['dataList']
        links = [x['href'] for x in resultList]
        return links

    def result_list_hebei(self, curl):
        response = requests.post(curl['url'],
                                 headers=curl['headers'],
                                 data=curl['data'],
                                 timeout=REQUEST_TIME_OUT,
                                 verify=False)
        resultList = json.loads(response.text)['page']['dataList']
        metadata_ids = [{
            'METADATA_ID': x['METADATA_ID'],
            'CREAT_DATE': x['CREAT_DATE'],
            'UPDATE_DATE': x['UPDATE_DATE'],
            'THEME_NAME': x['THEME_NAME']
        } for x in resultList]
        return metadata_ids

    def result_list_neimenggu(self, curl):
        response = requests.post(curl['url'],
                                 headers=curl['headers'],
                                 data=curl['data'],
                                 timeout=REQUEST_TIME_OUT,
                                 verify=False)
        resultList = json.loads(response.text)['data']
        ids = [x['id'] for x in resultList]
        return ids

    def result_list_liaoning(self, curl):
        response = requests.get(curl['url'], params=curl['queries'], headers=curl['headers'], timeout=REQUEST_TIME_OUT)
        html = response.content
        soup = BeautifulSoup(html, "html.parser")
        links = []
        for title in soup.find_all('div', attrs={'class': 'cata-title'}):
            link = title.find('a', attrs={'href': re.compile("/oportal/catalog/*")})
            links.append(link['href'])
        return links

    def result_list_shandong(self, curl):
        response = requests.get(curl['url'], params=curl['params'], headers=curl['headers'], timeout=REQUEST_TIME_OUT)
        html = response.content
        soup = BeautifulSoup(html, "html.parser")
        links = []
        for title in soup.find_all('div', attrs={'class': 'cata-title'}):
            link = title.find('a', attrs={'href': re.compile("/portal/catalog/*")})
            links.append(link['href'])
        return links

    def result_list_jiangsu(self, curl):
        response = requests.post(curl['url'],
                                 data=curl['data'],
                                 headers=curl['headers'],
                                 timeout=REQUEST_TIME_OUT,
                                 verify=False)
        resultList = json.loads(response.text)['custom']['resultList']
        rowGuids = [x['rowGuid'] for x in resultList]
        return rowGuids

    def result_list_shanghai(self, curl):
        response = requests.post(curl['url'], headers=curl['headers'], data=curl['data'], timeout=REQUEST_TIME_OUT)
        resultList = json.loads(response.text)['data']['content']
        dataset_ids = [{'datasetId': x['datasetId'], 'datasetName': x['datasetName']} for x in resultList]
        return dataset_ids

    def result_list_zhejiang(self, curl):
        response = requests.post(curl['url'], data=curl['data'], headers=curl['headers'], timeout=REQUEST_TIME_OUT)
        html = json.loads(response.text)['data']
        soup = BeautifulSoup(html, "html.parser")
        iids = []
        for title in soup.find_all('div', attrs={'class': 'search_result'}):
            link = title.find('a', attrs={'href': re.compile("../detail/data.do*")})
            parsed_link = urllib.parse.urlparse(link['href'])
            querys = urllib.parse.parse_qs(parsed_link.query)
            querys = {k: v[0] for k, v in querys.items()}
            iids.append(querys)
        return iids

    def result_list_anhui(self, curl):
        response = requests.post(curl['url'],
                                 data=curl['data'],
                                 headers=curl['headers'],
                                 verify=False,
                                 timeout=REQUEST_TIME_OUT)
        resultList = json.loads(response.text)['data']['rows']
        rids = [x['rid'] for x in resultList]
        return rids

    def result_list_jiangxi(self, curl):
        response = requests.post(curl['url'], json=curl['data'], headers=curl['headers'], timeout=REQUEST_TIME_OUT)
        resultList = json.loads(response.text)['data']
        data_ids = [x['dataId'] for x in resultList]
        return data_ids

    def result_list_fujian(self, curl):
        response = requests.get(curl['url'], params=curl['queries'], headers=curl['headers'], timeout=REQUEST_TIME_OUT)
        html = response.content
        soup = BeautifulSoup(html, "html.parser")
        links = []
        for title in soup.find_all('div', attrs={'class': 'mrline1-title'}):
            link = title.find('a', attrs={'href': re.compile("/oportal/catalog/*")})
            links.append(link['href'])
        return links

    def result_list_guangdong(self, curl):
        response = requests.post(curl['url'], json=curl['data'], headers=curl['headers'], timeout=REQUEST_TIME_OUT)
        resultList = json.loads(response.text)['data']['page']['list']
        res_ids = [x['resId'] for x in resultList]
        return res_ids

    def result_list_guangxi(self, curl):
        response = requests.get(curl['url'], params=curl['queries'], headers=curl['headers'], timeout=REQUEST_TIME_OUT)
        html = response.content
        soup = BeautifulSoup(html, "html.parser")
        links = []
        for title in soup.find_all('div', attrs={'class': 'cata-title'}):
            link = title.find('a', attrs={'href': re.compile("/portal/catalog/*")})
            links.append(link['href'])
        return links

    def result_list_hainan(self, curl):
        response = requests.post(curl['url'], data=curl['data'], headers=curl['headers'], timeout=REQUEST_TIME_OUT)
        resultList = json.loads(response.text)['data']['content']
        res_ids = [x['id'] for x in resultList]
        return res_ids

    def result_list_ningxia(self, curl):
        response = requests.get(curl['url'],
                                params=curl['queries'],
                                cookies=curl['cookies'],
                                headers=curl['headers'],
                                verify=False,
                                timeout=REQUEST_TIME_OUT)
        html = response.content
        soup = BeautifulSoup(html, "html.parser")
        links = []
        for title in soup.find_all('div', attrs={'class': 'cata-title'}):
            link = title.find('a', attrs={'href': re.compile("/portal/catalog/*")})
            links.append(link['href'])
        return links

    def result_list_shaanxi(self, curl):
        response = requests.get(curl['url'],
                                params=curl['queries'],
                                headers=curl['headers'],
                                verify=False,
                                timeout=REQUEST_TIME_OUT)
        resultList = json.loads(response.text)[0]['result']
        ids = [x['id'] for x in resultList]
        return ids

    def result_list_sichuan(self, curl):
        response = requests.get(curl['url'], params=curl['queries'], headers=curl['headers'], timeout=REQUEST_TIME_OUT)
        html = response.content
        soup = BeautifulSoup(html, "html.parser")
        links = []
        for title in soup.find_all('div', attrs={'class': 'cata-title'}):
            link = title.find('a', attrs={'href': re.compile("/oportal/catalog/*")})
            links.append(link['href'])
        return links

    def result_list_guizhou(self, curl):
        response = requests.post(curl['url'],
                                 json=curl['data'],
                                 headers=curl['headers'],
                                 verify=False,
                                 timeout=REQUEST_TIME_OUT)
        print(response)
        resultList = json.loads(response.text)['data']
        ids = [x['id'] for x in resultList]
        return ids

    def result_list_other(self):
        print("暂无该省")
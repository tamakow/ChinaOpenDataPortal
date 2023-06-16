import json
import time
import urllib

from tqdm import tqdm

from constants import (METADATA_SAVE_PATH, PROVINCE_CURL_JSON_PATH,
                       PROVINCE_LIST)
from detail import Detail
from resultlist import ResultList

curls = {}


class Crawler:
    def __init__(self, province, city):
        self.province = province
        self.city = city
        self.result_list = ResultList(self.province, self.city)
        self.detail = Detail(self.province, self.city)
        self.result_list_curl = curls[province][city]['resultList']
        self.detail_list_curl = curls[province][city]['detail']
        self.metadata_list = []

    def crawl(self):
        func_name = f"crawl_{str(self.province)}_{str(self.city)}"
        func = getattr(self, func_name, self.crawl_other)
        func()

    # TODO: 反爬虫 ConnectionResetError: [WinError 10054]
    def crawl_sichuan_sichuan(self):
        for page in tqdm(range(1, 1249)):
            # print(page)
            curl = self.result_list_curl.copy()
            curl['queries']['page'] = str(page)
            links = self.result_list.get_result_list(curl)
            if len(links) == 0:
                break
            for link in links:
                curl = self.detail_list_curl.copy()
                curl['url'] += link['link']
                metadata = self.detail.get_detail(curl)
                if bool(metadata):
                    metadata['数据格式'] = link['data_formats'] if link['data_formats'] != '[]' else "[file]"
                    metadata['详情页网址'] = curl['url']
                    print(metadata)
                    self.metadata_list.append(metadata)

    def crawl_sichuan_chengdu(self):
        for page in tqdm(range(1, 704)):
        # for page in range(1, 704):
        #     print(page)
            curl = self.result_list_curl.copy()
            curl['queries']['page'] = str(page)
            links = self.result_list.get_result_list(curl)
            if len(links) == 0:
                break
            for link in links:
                curl = self.detail_list_curl.copy()
                curl['url'] += link['link']
                metadata = self.detail.get_detail(curl)
                if bool(metadata):
                    metadata['数据格式'] = link['data_formats'] if link['data_formats'] != '[]' else "[file]"
                    metadata['详情页网址'] = curl['url']
                    # print(metadata)
                    self.metadata_list.append(metadata)

    def crawl_sichuan_zigong(self):
        for page in range(1, 870):
            print(page)
            curl = self.result_list_curl.copy()
            curl['queries']['offset'] = (page - 1) * 10
            ids = self.result_list.get_result_list(curl)


    def crawl_guizhou_guizhou(self):
        for page in range(1, 5):
            print(page)
            curl = self.result_list_curl.copy()
            curl['data']['pageIndex'] = page
            ids = self.result_list.get_result_list(curl)
            for id in ids:
                curl = self.detail_list_curl.copy()
                curl['data']['id'] = id
                metadata = self.detail.get_detail(curl)
                print(metadata)
                self.metadata_list.append(metadata)


    def crawl_other(self):
        print("暂无该省")

    def save_matadata_as_json(self, save_dir):
        filename = save_dir + self.province + '_' + self.city + '.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.metadata_list, f, ensure_ascii=False)


if __name__ == '__main__':
    provinces = PROVINCE_LIST
    with open(PROVINCE_CURL_JSON_PATH, 'r', encoding='utf-8') as curlFile:
        curls = json.load(curlFile)

    crawler = Crawler("sichuan", "zigong")
    crawler.crawl()
    crawler.save_matadata_as_json(METADATA_SAVE_PATH)
    # for province in provinces:
    #     crawler = Crawler(province)
    #     crawler.crawl()

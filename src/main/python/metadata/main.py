import json
import urllib

from constants import PROVINCE_CURL_JSON_PATH, PROVINCE_LIST
from detail import Detail
from resultlist import ResultList

province_curls = {}


class Crawler:
    def __init__(self, province):
        self.province = province
        self.result_list = ResultList(self.province)
        self.detail = Detail(self.province)
        self.result_list_curl = province_curls[province]['resultList']
        self.detail_list_curl = province_curls[province]['detail']
        self.metadata_list = []

    def crawl(self):
        func_name = "crawl_" + str(self.province)
        func = getattr(self, func_name, self.crawl_other)
        func()

    # TODO: 反爬虫 ConnectionResetError: [WinError 10054]
    def crawl_beijing(self):
        for page in range(1, 2):
            print(page)
            curl = self.result_list_curl.copy()
            curl['data']['curPage'] = str(page)
            links = self.result_list.get_result_list(curl)
            for link in links:
                curl = self.detail_list_curl.copy()
                curl['url'] = link
                metadata = self.detail.get_detail(curl)
                print(metadata)
                self.metadata_list.append(metadata)

    def crawl_tianjin(self):
        curl = self.result_list_curl.copy()
        links = self.result_list.get_result_list(curl)
        for link in links[:10]:
            curl = self.detail_list_curl.copy()
            curl['url'] = link
            metadata = self.detail.get_detail(curl)
            print(metadata)
            self.metadata_list.append(metadata)

    def crawl_hebei(self):
        for page in range(1, 5):
            print(page)
            curl = self.result_list_curl.copy()
            curl['data']['pageNo'] = str(page)
            metadata_ids = self.result_list.get_result_list(curl)
            for metadata_id in metadata_ids:
                curl = self.detail_list_curl.copy()
                curl['data']['rowkey'] = metadata_id['METADATA_ID']
                curl['data']['list_url'] = curl['data']['list_url'].format(page)
                metadata = self.detail.get_detail(curl)
                metadata['所属主题'] = metadata_id['THEME_NAME']
                metadata['发布时间'] = metadata_id['CREAT_DATE']
                metadata['更新日期'] = metadata_id['UPDATE_DATE']
                print(metadata)
                self.metadata_list.append(metadata)

    def crawl_neimenggu(self):
        for page in range(1, 5):
            print(page)
            curl = self.result_list_curl.copy()
            curl['data']['page'] = str(page)
            ids = self.result_list.get_result_list(curl)
            for id in ids:
                curl = self.detail_list_curl.copy()
                curl['data']['id'] = id
                metadata = self.detail.get_detail(curl)
                print(metadata)
                self.metadata_list.append(metadata)

    def crawl_liaoning(self):
        for page in range(1, 5):
            print(page)
            curl = self.result_list_curl.copy()
            curl['queries']['page'] = str(page)
            links = self.result_list.get_result_list(curl)
            for link in links:
                curl = self.detail_list_curl.copy()
                curl['url'] += link
                metadata = self.detail.get_detail(curl)
                print(metadata)
                self.metadata_list.append(metadata)

    def crawl_shandong(self):
        for page in range(1, 5):
            print(page)
            curl = self.result_list_curl.copy()
            curl['params']['page'] = str(page)
            links = self.result_list.get_result_list(curl)
            for link in links:
                curl = self.detail_list_curl.copy()
                curl['url'] += link
                metadata = self.detail.get_detail(curl)
                print(metadata)
                self.metadata_list.append(metadata)

    def crawl_jiangsu(self):
        for city in ['', 'all']:
            for page in range(0, 10):
                print(page)
                curl = self.result_list_curl.copy()
                curl['data'] = curl['data'].format(page, city)
                rowGuids = self.result_list.get_result_list(curl)
                for rowGuid in rowGuids:
                    curl = self.detail_list_curl.copy()
                    curl['url'] = curl['url'].format(rowGuid)
                    curl['data'] = curl['data'].format(rowGuid)
                    metadata = self.detail.get_detail(curl)
                    print(metadata)
                    self.metadata_list.append(metadata)

    def crawl_shanghai(self):
        for page in range(1, 5):
            print(page)
            curl = self.result_list_curl.copy()
            curl['data'] = curl['data'].replace('\"pageNum\":1', f'\"pageNum\":{page}').encode()
            dataset_ids = self.result_list.get_result_list(curl)
            for dataset_id in dataset_ids:
                curl = self.detail_list_curl.copy()
                curl['headers']['Referer'] = curl['headers']['Referer'].format(
                    dataset_id['datasetId'], urllib.parse.quote(dataset_id['datasetName']))
                curl['url'] = curl['url'].format(dataset_id['datasetId'])
                metadata = self.detail.get_detail(curl)
                print(metadata)
                self.metadata_list.append(metadata)

    def crawl_zhejiang(self):
        for page in range(1, 5):
            print(page)
            curl = self.result_list_curl.copy()
            curl['data']['pageNumber'] = str(page)
            iids = self.result_list.get_result_list(curl)
            for iid in iids:
                curl = self.detail_list_curl.copy()
                curl['queries'] = iid
                metadata = self.detail.get_detail(curl)
                print(metadata)
                self.metadata_list.append(metadata)

    def crawl_anhui(self):
        for page in range(1, 5):
            print(page)
            curl = self.result_list_curl.copy()
            curl['data']['pageNum'] = str(page)
            rids = self.result_list.get_result_list(curl)
            for rid in rids:
                curl = self.detail_list_curl.copy()
                curl['headers']['Referer'] = curl['headers']['Referer'].format(rid)
                curl['data']['rid'] = rid
                metadata = self.detail.get_detail(curl)
                print(metadata)
                self.metadata_list.append(metadata)

    def crawl_jiangxi(self):
        for page in range(1, 5):
            print(page)
            curl = self.result_list_curl.copy()
            curl['data']['current'] = page
            data_ids = self.result_list.get_result_list(curl)
            for data_id in data_ids:
                curl = self.detail_list_curl.copy()
                curl['headers']['Referer'] = curl['headers']['Referer'].format(data_id)
                curl['queries']['dataId'] = data_id
                metadata = self.detail.get_detail(curl)
                print(metadata)
                self.metadata_list.append(metadata)

    def crawl_fujian(self):
        for page in range(1, 5):
            print(page)
            curl = self.result_list_curl.copy()
            curl['queries']['page'] = str(page)
            links = self.result_list.get_result_list(curl)
            for link in links:
                curl = self.detail_list_curl.copy()
                curl['url'] += link
                metadata = self.detail.get_detail(curl)
                print(metadata)
                self.metadata_list.append(metadata)

    def crawl_guangdong(self):
        for page in range(1, 5):
            print(page)
            curl = self.result_list_curl.copy()
            curl['data']['pageNo'] = page
            res_ids = self.result_list.get_result_list(curl)
            for res_id in res_ids:
                curl = self.detail_list_curl.copy()
                curl['data']['resId'] = res_id
                metadata = self.detail.get_detail(curl)
                print(metadata)
                self.metadata_list.append(metadata)

    def crawl_guangxi(self):
        for page in range(1, 5):
            print(page)
            curl = self.result_list_curl.copy()
            curl['queries']['page'] = str(page)
            links = self.result_list.get_result_list(curl)
            for link in links:
                curl = self.detail_list_curl.copy()
                curl['url'] += link
                metadata = self.detail.get_detail(curl)
                print(metadata)
                self.metadata_list.append(metadata)

    def crawl_hainan(self):
        for page in range(0, 5):
            print(page)
            curl = self.result_list_curl.copy()
            curl['data']['curPage'] = page
            ids = self.result_list.get_result_list(curl)
            for id in ids:
                curl = self.detail_list_curl.copy()
                curl['url'] = curl['url'].format(id)
                metadata = self.detail.get_detail(curl)
                print(metadata)
                self.metadata_list.append(metadata)

    def crawl_ningxia(self):
        for page in range(1, 5):
            print(page)
            curl = self.result_list_curl.copy()
            curl['queries']['page'] = str(page)
            links = self.result_list.get_result_list(curl)
            for link in links:
                curl = self.detail_list_curl.copy()
                curl['url'] += link
                metadata = self.detail.get_detail(curl)
                print(metadata)
                self.metadata_list.append(metadata)

    def crawl_shaanxi(self):
        for page in range(1, 5):
            print(page)
            curl = self.result_list_curl.copy()
            curl['queries']['page.pageNo'] = str(page)
            ids = self.result_list.get_result_list(curl)
            for id in ids:
                curl = self.detail_list_curl.copy()
                curl['queries']['id'] = str(id)
                metadata = self.detail.get_detail(curl)
                print(metadata)
                self.metadata_list.append(metadata)

    def crawl_sichuan(self):
        for page in range(1, 5):
            print(page)
            curl = self.result_list_curl.copy()
            curl['queries']['page'] = str(page)
            links = self.result_list.get_result_list(curl)
            for link in links:
                curl = self.detail_list_curl.copy()
                curl['url'] += link
                metadata = self.detail.get_detail(curl)
                print(metadata)
                self.metadata_list.append(metadata)

    def crawl_guizhou(self):
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


if __name__ == '__main__':
    provinces = PROVINCE_LIST
    with open(PROVINCE_CURL_JSON_PATH, 'r', encoding='utf-8') as curlFile:
        province_curls = json.load(curlFile)

    crawler = Crawler("liaoning")
    crawler.crawl()
    # for province in provinces:
    #     crawler = Crawler(province)
    #     crawler.crawl()

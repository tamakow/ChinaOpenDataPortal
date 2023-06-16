import json
import re
import time
import unicodedata as ucd

import requests
from bs4 import BeautifulSoup
from constants import REQUEST_TIME_OUT


class Detail:
    def __init__(self, province, city) -> None:
        self.province = province
        self.city = city

    def get_detail(self, curl):
        func_name = f"detail_{str(self.province)}_{str(self.city)}"
        func = getattr(self, func_name, self.detail_other)
        return func(curl)

    def detail_sichuan_sichuan(self, curl):

        list_fields = ["来源部门", "重点领域", "发布时间", "更新时间", "开放条件"]
        table_fields = ["数据量", "所属行业", "更新频率", "部门电话", "部门邮箱", "标签", "描述"]
        response = requests.get(curl['url'], headers=curl['headers'], timeout=REQUEST_TIME_OUT)
        if response.status_code != requests.codes.ok:
            print("error " + str(response.status_code) + ": " + curl['url'])
            return dict()
        html = response.content.decode('utf-8')
        soup = BeautifulSoup(html, "html.parser")
        dataset_metadata = {}
        title = soup.find('ul', attrs={'class': 'd-title pull-left'})
        title = title.find('h4').get_text()
        dataset_metadata['标题'] = title
        for li in soup.find('ul', attrs={'class': 'list-inline'}).find_all('li', attrs={}):
            li_name = li.get_text().split('：')[0].strip()
            if li_name in list_fields:
                li_text = li.find('span', attrs={'class': 'text-primary'}).get_text().strip()
                dataset_metadata[li_name] = li_text
        table = soup.find('li', attrs={'name': 'basicinfo'})
        for td_name in table_fields:
            td_text = table.find('td', text=td_name)
            if td_text is not None:
                td_text = td_text.find_next('td').get_text().strip()
                td_text = ucd.normalize('NFKC', td_text).replace(' ', '')
                dataset_metadata[td_name] = td_text
        dataset_metadata['详情页网址'] = curl['url']
        return dataset_metadata

    def detail_sichuan_chengdu(self, curl):
        list_fields = ["来源部门", "主题", "发布时间", "更新时间", "开放条件"]
        table_fields = ["数据量", "所属行业", "更新频率", "部门电话", "部门邮箱", "标签", "描述"]
        response = requests.get(curl['url'], headers=curl['headers'], timeout=REQUEST_TIME_OUT)
        if response.status_code != requests.codes.ok:
            print("error " + str(response.status_code) + ": " + curl['url'])
            return dict()
        html = response.content.decode('utf-8')
        soup = BeautifulSoup(html, "html.parser")
        dataset_metadata = {}
        title = soup.find('ul', attrs={'class': 'd-title pull-left'})
        title = title.find('h4').get_text()
        dataset_metadata['标题'] = title
        for li in soup.find('ul', attrs={'class': 'list-inline'}).find_all('li', attrs={}):
            li_name = li.get_text().split('：')[0].strip()
            if li_name in list_fields:
                li_text = li.find('span', attrs={'class': 'text-primary'}).get_text().strip()
                dataset_metadata[li_name] = li_text
        table = soup.find('li', attrs={'name': 'basicinfo'})
        for td_name in table_fields:
            td_text = table.find('td', text=td_name)
            if td_text is not None:
                td_text = td_text.find_next('td').get_text().strip()
                td_text = ucd.normalize('NFKC', td_text).replace(' ', '')
                dataset_metadata[td_name] = td_text
        return dataset_metadata


    def detail_guizhou_guizhou(self, curl):

        key_map = {
            'name': "标题",
            'description': "数据摘要",
            'topicName': "主题名称",
            'orgName': "数据提供方",
            'industryName': "所属行业",
            'updateTime': "更新时间",
            'createTime': "发布时间",
            'openAttribute': "开放属性",
            'frequency': "更新频率",
        }

        frequency_mapping = {0: "每年", 1: "每季度", 2: "每月", 3: "每周", 4: "每天", 5: "实时", 6: "每半年"}

        response = requests.post(curl['url'], json=curl['data'], headers=curl['headers'], timeout=REQUEST_TIME_OUT)

        dataset_matadata = {}
        detail_json = json.loads(response.text)['data']
        for key, value in key_map.items():
            if key in ['updateTime', 'createTime']:
                detail_json[key] = time.strftime("%Y-%m-%d", time.localtime(detail_json[key] / 1000))
            if key == 'frequency':
                detail_json[key] = frequency_mapping[detail_json[key]]
            if key == 'openAttribute':
                detail_json[key] = "有条件开放" if detail_json[key] == 1 else "无条件开放"
            dataset_matadata[value] = detail_json[key]
        return dataset_matadata

    def detail_other(self, curl):
        print("暂无该省市")
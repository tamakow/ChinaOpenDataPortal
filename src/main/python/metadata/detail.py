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

    def detail_sichuan_panzhihua(self, curl):

        list_fields = ["来源部门", "重点领域", "发布时间", "更新时间", "开放类型"]
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

    def detail_sichuan_zigong(self, curl):

        key_map = {
            'catalogTitle': "标题",
            'catalogDesc': "描述",
            'supplyOrg': "来源部门",
            'domainName': "主题",
            'createdTime': "发布时间",
            'modifiedTime': "更新时间",
            'isOpen': "开放条件",
            'industryName': "所属行业",
            'updateCycle': "更新频率",
            'tel': "部门电话"
        }

        response = requests.get(curl['url'], params=curl['queries'], headers=curl['headers'], timeout=REQUEST_TIME_OUT)
        if response.status_code != requests.codes.ok:
            print("error " + str(response.status_code) + ": " + curl['url'])
            return dict()

        dataset_matadata = {}
        detail_json = json.loads(response.text)['data'][0]
        for key, value in key_map.items():
            if key in ['modifiedTime', 'createdTime']:
                detail_json[key] = time.strftime("%Y-%m-%d", time.localtime(detail_json[key] / 1000))
            if key == 'isOpen':
                detail_json[key] = "有条件开放" if detail_json[key] == "0" else "无条件开放"
            dataset_matadata[value] = detail_json[key]
        return dataset_matadata

    def detail_sichuan_luzhou(self, curl):

        list_fields = ["提供方", "数据主题", "数据领域", "联系电话"]
        table_fields = ["更新周期", "关键字", "资源摘要"]
        response = requests.get(curl['url'], params=curl['queries'], headers=curl['headers'], timeout=REQUEST_TIME_OUT)
        if response.status_code != requests.codes.ok:
            print("error " + str(response.status_code) + ": " + curl['url'])
            return dict()
        html = response.content.decode('utf-8')
        soup = BeautifulSoup(html, "html.parser")
        dataset_metadata = {}
        title = soup.find('h2', attrs={'class': 'dt-name'})
        title = title.find('p').get_text()
        dataset_metadata['标题'] = title
        for li in soup.find('ul', attrs={'class': 'desc-list-info clearfix'}).find_all('li', attrs={}):
            li_name = li.find('span').get_text().split('：')[0].strip()
            if li_name in list_fields:
                li_text = li.find_all('span')[1].get_text().strip()
                dataset_metadata[li_name] = li_text
        table = soup.find('table', attrs={'class': 'table table-striped table-bordered table-advance table-hover'})
        for td_name in table_fields:
            td_text = table.find('td', text=td_name)
            if td_text is not None:
                td_text = td_text.find_next('td').get_text().strip()
                td_text = ucd.normalize('NFKC', td_text).replace(' ', '')
                dataset_metadata[td_name] = td_text
        return dataset_metadata


    def detail_sichuan_deyang(self, curl):

        key_map = {
            'xxzymc': "标题",
            'xxzytgf': "资源提供方",
            'ssztlmmc': "领域名称",
            'fbrq': "发布时间",
            'gxrq': "更新时间",
            'kflx': "开放类型",  # "01": "有条件开放", "02": "无条件开放"
            'sjl': "数据量",
            'ssqtlmmc': "所属行业",
            'gxzq': "更新周期",
            'zjhm': "联系电话",
            'mlbqmcList': "标签",
            'zyzy': "资源摘要",
            'zygs': "资源格式"
        }

        frequency_mapping = {'01': "每日", '02': "每周", '03': "每月", '04': "季度", '05': "年"}

        response = requests.get(curl['url'], params=curl['queries'], headers=curl['headers'], timeout=REQUEST_TIME_OUT)
        if response.status_code != requests.codes.ok:
            print("error " + str(response.status_code) + ": " + curl['url'])
            return dict()

        dataset_matadata = {}
        detail_json = json.loads(response.text)['data']
        for key, value in key_map.items():
            if key in ['fbrq', 'gxrq']:
                detail_json[key] = time.strftime("%Y-%m-%d", time.localtime(int(detail_json[key]) / 1000))
            if key == 'kflx':
                detail_json[key] = "有条件开放" if detail_json[key] == "01" else "无条件开放"
            if key == 'gxzq':
                detail_json[key] = frequency_mapping[detail_json[key]]
            if key == 'zygs':
                detail_json[key] = str(detail_json[key].split('\\'))
            dataset_matadata[value] = detail_json[key]
        return dataset_matadata

    def detail_sichuan_mianyang(self, curl):

        key_map = {
            'dir_name': "标题",
            'dir_office': "提供部门",
            'sszt': "领域",
            'gmt_modified': "更新时间",
            'sshy': "所属行业",
            'dir_updatetime': "更新频率",
            'dir_phone': "联系电话",
            'ssbq': "标签",
        }

        frequency_mapping = {'0': "实时", '1': "每日", '2': "每周", '3': "每月", '4': "每季度", '5': "每半年", '6': "每年"}

        response = requests.get(curl['url'], params=curl['queries'], headers=curl['headers'], timeout=REQUEST_TIME_OUT)
        if response.status_code != requests.codes.ok:
            print("error " + str(response.status_code) + ": " + curl['url'])
            return dict()

        dataset_matadata = {}
        detail_json = json.loads(response.text)['elementthing']['showBasicList']
        share_level = detail_json['dir_statistics_data'][0]['sharelevel']
        if share_level == '0':
            dataset_matadata['开放类型'] = "无条件开放"
        elif share_level == '1':
            dataset_matadata['开放类型'] = "有条件开放"
        else:
            dataset_matadata['开放类型'] = "不予开放"
        for key, value in key_map.items():
            if key == 'gmt_modified':
                detail_json[key] = detail_json[key].split(" ")[0].strip()
            if key == 'dir_updatetime':
                detail_json[key] = frequency_mapping[detail_json[key]]
            dataset_matadata[value] = detail_json[key]
        return dataset_matadata

    def detail_sichuan_guangyuan(self, curl):

        key_map = {
            'name': "标题",
            'department': "资源提供单位",
            'add_time': "发布时间",
            'release_time': "更新时间",
            'SharedStructuredRecords': "开放类型",
            'cycle': "更新频率",
            'PHONE': "联系电话",
            'remarks': "资源摘要",
            'resourcrtype': "资源格式"
        }

        frequency_mapping = {'8': "实时", '1': "其他", '2': "每日", '3': "每周", '4': "每月", '5': "每季度", '6': "每半年", '7': "每年"}

        response = requests.post(curl['url'], json=curl['data'], headers=curl['headers'], timeout=REQUEST_TIME_OUT)
        if response.status_code != requests.codes.ok:
            print("error " + str(response.status_code) + ": " + curl['url'])
            return dict()

        dataset_matadata = {}
        detail_json = json.loads(response.text)['data']['details'][0]
        for key, value in key_map.items():
            if key in ['add_time', 'release_time']:
                detail_json[key] = detail_json[key].split(" ")[0].strip()
            if key == 'cycle':
                if key in detail_json:
                    detail_json[key] = frequency_mapping[detail_json[key]] if detail_json[key] in frequency_mapping else "其他"
                else:
                    detail_json[key] = '其他'
            if key == 'SharedStructuredRecords':
                detail_json[key] = "有条件开放" if detail_json[key] == '1' else "无条件开放"
            if key == 'resourcrtype':
                detail_json[key] = "['api']" if detail_json[key] == "数据库" else "['file']"
            dataset_matadata[value] = detail_json[key]
        return dataset_matadata

    def detail_sichuan_suining(self, curl):

        key_map = {
            'xxzymc': "标题",
            'xxzytgf': "资源提供方",
            'sslymc': "领域名称",
            'fbrq': "发布时间",
            'gxrq': "更新时间",
            'kflx': "开放类型",  # "01": "有条件开放", "02": "无条件开放"
            'sshy': "所属行业",
            'gxzq': "更新周期",
            'zjhm': "联系电话",
            'mlbqmcList': "标签",
            'zyzy': "资源摘要",
        }

        frequency_mapping = {'01': "每日", '02': "每周", '03': "每月", '04': "季度", '05': "年", '06': "半年"}

        response = requests.get(curl['url'], params=curl['queries'], headers=curl['headers'], timeout=REQUEST_TIME_OUT)
        if response.status_code != requests.codes.ok:
            print("error " + str(response.status_code) + ": " + curl['url'])
            return dict()

        dataset_matadata = {}
        detail_json = json.loads(response.text)['data']
        for key, value in key_map.items():
            if key in ['fbrq', 'gxrq']:
                detail_json[key] = time.strftime("%Y-%m-%d", time.localtime(int(detail_json[key]) / 1000))
            if key == 'kflx':
                detail_json[key] = "有条件开放" if detail_json[key] == "01" else "无条件开放"
            if key == 'gxzq':
                detail_json[key] = frequency_mapping[detail_json[key]]
            dataset_matadata[value] = detail_json[key]
        return dataset_matadata

    def detail_sichuan_neijiang(self, curl):

        key_map = {
            'catalogName': "标题",
            'departmentName': "来源部门",
            'topicNameList': "主题",
            'createdDate': "发布时间",
            'lastUpdatedDate': "更新时间",
            'openTypeValue': "开放条件",
            'dataNum': "数据量",
            'industryName': "行业名称",
            'accessFrequency': "更新频率",
            'departPhone': "技术支持电话",
            'departEmail': "技术支持邮箱",
            'resourceFormatValue': "资源格式",
            'catalogDesc': "描述",
        }

        response = requests.post(curl['url'], json=curl['data'], headers=curl['headers'], timeout=REQUEST_TIME_OUT)
        if response.status_code != requests.codes.ok:
            print("error " + str(response.status_code) + ": " + curl['url'])
            return dict()

        dataset_matadata = {}
        detail_json = json.loads(response.text)['data']
        for key, value in key_map.items():
            if key in ['createdDate', 'lastUpdatedDate']:
                detail_json[key] = time.strftime("%Y-%m-%d", time.localtime(int(detail_json[key]) / 1000))
            dataset_matadata[value] = detail_json[key]
        return dataset_matadata

    def detail_sichuan_leshan(self, curl):

        key_map = {
            'resourceName': "标题",
            'resourceProvider': "来源部门",
            'associativeClassification': "领域名称",
            'publishTime': "发布时间",
            'updateTime': "更新时间",
            'sharedType': "开放属性",
            'industryClassification': "行业名称",
            'updateCycle': "更新频率",
            'resourceFormat': "资源格式",
            'remark': "描述",
        }

        response = requests.get(curl['url'], params=curl['queries'], headers=curl['headers'], timeout=REQUEST_TIME_OUT)
        if response.status_code != requests.codes.ok:
            print("error " + str(response.status_code) + ": " + curl['url'])
            return dict()

        dataset_matadata = {}
        detail_json = json.loads(response.text)['data']
        for key, value in key_map.items():
            if key == 'publishTime':
                detail_json[key] = detail_json[key].split(" ")[0].strip()
            if key == 'updateTime':
                if bool(detail_json[key]):
                    detail_json[key] = detail_json[key].split(" ")[0].strip()
                else:
                    detail_json[key] = detail_json['publishTime']
            if key == 'resourceFormat':
                if detail_json == 'doc':
                    detail_json[key] = ['doc', 'docx', 'xls', 'xml', 'json', 'csv']
                else:
                    detail_json[key] = ['xls', 'xml', 'json', 'csv']
            dataset_matadata[value] = detail_json[key]
        return dataset_matadata

    def detail_sichuan_nanchong(self, curl):

        key_map = {
            'NAME': "标题",
            'PROVIDEDEPT': "资源提供单位信息",
            'TAG_ID1': "领域名称",
            'CREATETIME': "发布时间",
            'UPDATE_TIME': "更新时间",
            'OPENTYPE': "开放条件",
            'RESOURCESNUM': "数据量",
            'TAG_ID2': "行业名称",
            'FORMATNAME': "资源格式",
            'ABSRACTINFO': "描述",
        }

        response = requests.get(curl['url'], params=curl['queries'], headers=curl['headers'], timeout=REQUEST_TIME_OUT)
        if response.status_code != requests.codes.ok:
            print("error " + str(response.status_code) + ": " + curl['url'])
            return dict()

        dataset_matadata = {}
        detail_json = json.loads(response.text)['data'][0]

        provide_detail = detail_json['provideDetail']
        if provide_detail == '':
            dataset_matadata["部门电话"] = ''
            dataset_matadata["部门邮箱"] = ''
        else:
            dataset_matadata["部门电话"] = provide_detail['PHONENUM']
            dataset_matadata["部门邮箱"] = provide_detail['EMAIL']

        for key, value in key_map.items():
            if key in ['CREATETIME', 'UPDATE_TIME']:
                detail_json[key] = detail_json[key].split(" ")[0].strip()
            if key == 'OPENTYPE':
                detail_json[key] = "无条件开放" if detail_json[key] == 1 else "有条件开放"
            if key == 'FORMATNAME':
                detail_json[key] = detail_json[key].lower()
            dataset_matadata[value] = detail_json[key]
        return dataset_matadata

    def detail_ningxia_ningxia(self, curl):

        list_fields = ["来源部门", "重点领域", "发布时间", "更新时间", "开放条件"]
        table_fields = ["所属行业", "更新频率", "部门电话", "部门邮箱", "标签", "描述"]
        response = requests.get(curl['url'], headers=curl['headers'], timeout=REQUEST_TIME_OUT, verify=False)
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

    def detail_xinjiang_wlmq(self, curl):

        list_fields = ["来源部门", "所属主题", "发布时间", "最后更新", "开放状态", "所属行业", "更新频率", "标签", "描述"]
        response = requests.get(curl['url'], params=curl['queries'], headers=curl['headers'], timeout=REQUEST_TIME_OUT)
        if response.status_code != requests.codes.ok:
            print("error " + str(response.status_code) + ": " + curl['url'])
            return dict()
        html = response.content.decode('utf-8')
        soup = BeautifulSoup(html, "html.parser")
        dataset_metadata = {}
        title = soup.find('div', attrs={'class': 'detail-header'})
        title = title.find('span', attrs={'class': 'detail-title'}).get_text()
        dataset_metadata['标题'] = title

        for divs in soup.find('div', attrs={'class': 'detail-info-list tab-body'}).find('li', attrs={'action': 'data-info'}).find_all('div', attrs={'class': 'info-list'}):
            for li in divs.find_all('li'):
                li_name = li.find('div', attrs={'class': 'info-header'}).get_text().strip()
                if li_name in list_fields:
                    div = li.find('div', attrs={'class': 'info-body'})
                    li_text = div.get_text().strip()
                    if li_name == '标签':
                        li_text = div['tags']
                    if li_name in ["发布时间", "最后更新"]:
                        li_text = li_text.split(' ')[0].strip()
                    dataset_metadata[li_name] = li_text
        dataset_metadata['详情页网址'] = curl['url']
        return dataset_metadata

    def detail_other(self, curl):
        print("暂无该省市")

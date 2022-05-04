# -*- encoding "utf-8" -*-
# @Time : 2022/4/24 17:36
# @Author : PRQ
# @File :shoe.py

import csv
import requests
import json

with open('LN.csv', 'w') as f:
    csv_write = csv.writer(f)
    colName = ['title', 'MPrice', 'SPrice', 'SPUid', 'link', 'imgLink']
    csv_write.writerow(colName)
    f.close()

headers = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "content-length": "301",
    "content-type": "application/json;charset=UTF-8",
    "cookie": "NTKF_T2D_CLIENTID=guestABC5A3ED-B652-7720-2946-5A4D1686ABAB; nTalk_CACHE_DATA={"
              "uid:kf_9887_ISME9754_guestABC5A3ED-B652-77,tid:1650782443141084}",
    "device-type": "pc",
    "origin": "https://store.lining.com",
    "referer": "https://store.lining.com/",
    "sec-ch-ua": '''" Not A;Brand";v="99", "Chromium";v="100", "Microsoft Edge";v="100"''',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "tversion": "undefined",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.50",
    "Content-Type": "application/json",
}
url = "https://api.store.lining.com/goodsg/v1/goods-jh-query/search/lining/list/page"

shoes = {"男鞋": ['跑步鞋', '篮球鞋', '运动生活鞋', '训练鞋', '羽毛球鞋', '户外鞋', '凉鞋/拖鞋'],
         "女鞋": ['跑步鞋', '篮球鞋', '运动生活鞋', '训练鞋', '羽毛球鞋', '凉鞋/拖鞋']}
with open('LN.csv', 'a') as f:
    csv_write = csv.writer(f)
    for shoe in shoes.keys():
        for item in shoes[shoe]:
            get = True
            pageSize = 50
            pageNum = 1
            while get:
                data = {"source": "4", "saasId": "8324992625302181585", "pageNum": pageNum, "pageSize": pageSize,
                        "field": 'null',
                        "sortBy": 1, "query": "", "filter": {"tagsInfo": {
                        "customTag": [{"tagName": "firstCategory", "tagValue": ["运动鞋"]},
                                      {"tagName": "secondCategory", "tagValue": [shoe]},
                                      {"tagName": "thirdCategory", "tagValue": [item]}]}}}
                r = requests.post(url, headers=headers, data=json.dumps(data))
                info = json.loads(r.content.decode('utf-8'))
                dataList = info['data']['dataList']
                if len(dataList) < pageSize:
                    get = False
                elif len(dataList) == 0:
                    break
                else:
                    pageNum += 1
                for i in range(len(dataList)):
                    spuID = dataList[i]['spuId']
                    title = dataList[i]['title']
                    imgLink = dataList[i]['primaryImage']
                    link = "https://store.lining.com/goods/detail?spuId=" + spuID
                    MarketPrice = dataList[i]['spuPrice']['maxMarketPrice']
                    SalePrice = dataList[i]['spuPrice']['minSalePrice']
                    about = dataList[i]['spuVOList']
                    csv_write.writerow([title, MarketPrice, SalePrice, spuID, link, imgLink])
                    for j in about:
                        if j['spuId'] == spuID:
                            continue
                        else:
                            csv_write.writerow([title, MarketPrice, SalePrice, j['spuId'],
                                                    "https://store.lining.com/goods/detail?spuId=" + j['spuId'], j['primaryImage']])
    f.close()

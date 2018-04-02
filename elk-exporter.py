#!/usr/bin/env python
# -*- coding: utf-8 -*-
import elasticsearch
import query
from prometheus_client import start_http_server
import time
from datetime import datetime
from prometheus_client import Gauge

# 定义metrics，列表里边是labels的名称
elkErrorCount = Gauge('ELK_Error_Count', 'Error Level Count Of The Speicfic Index', ['index'])


def queryf(client, index, query):
    data = client.search(index=index, size=100, body=query)
    for hit in data['hits']['hits']:
        yield hit


# def getfield(item, fields):
#     data = dict()
#     for field in fields:
#         data.update({
#             field: item['_source'].get(field)
#         })
#     return data


def main():
    start_http_server(9102)
    client = elasticsearch.Elasticsearch(hosts=['10.104.255.201'],
                                         http_auth=('elastic', 'elastic'),
                                         port=9200)
    today = datetime.now().strftime("%Y.%m.%d")
    index_list = map(lambda x: x, ['*-api-gateway-*', '*-app-*', '*-credit-*', '*-passporter-*', '*-nginx-*',
                                        '*-order-*', '*-loan-*', '*-debt-*', '*-openapi-gateway-*'])

    querystring = '(level:"ERROR" OR nginx_responsecode:404 OR nginx_responsecode:403 OR nginx_responsecode:5* OR NOT httpCode:2*)'
    querys = query.Query(querystring, 'now-10s', 'now').__str__()
    while 1:
        counter = 0
        for i in index_list:
            print(i)
            item_generator = queryf(client, i, querys)
            try:
                item = next(item_generator)
                item['_source'].update({
                    '_index': item['_index']
                })
                counter += 1
            except StopIteration:
                pass
            finally:
                index = i
                print(counter, index)
                elkErrorCount.labels(index).set(counter)
        time.sleep(10)


if __name__ == '__main__':
    main()

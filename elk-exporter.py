#!/usr/bin/env python
# -*- coding: utf-8 -*-
import elasticsearch
import query
from prometheus_client import start_http_server
import time
from prometheus_client import Gauge
from searches.searches import Search


# 定义metrics，列表里边是labels的名称
nginxErrorCount = Gauge('Ng_Error_Count', 'Error Level Count Of Nginx', ['nginx_vhost', 'nginx_request_api'])
openapiErrorCount = Gauge('OpenApi_Error_Count', 'Error Level Count Of OpenApi', ['appId', 'url'])


def main():
    # 启动http服务
    start_http_server(9102)
    # 生成es客户端
    client = elasticsearch.Elasticsearch(hosts=['10.104.255.201'],
                                         http_auth=('elastic', 'elastic'),
                                         port=9200)
    # today = datetime.now().strftime("%Y.%m.%d")
    index_list = ['*-nginx-proxy-*', '*-order-access-*']
    fields_nginx = ['nginx_vhost', 'nginx_request_api']
    fields_openapi = ['appId', 'url']
    querystring_nginx = '(nginx_responsecode:404 OR nginx_responsecode:403 OR nginx_responsecode:5*)'
    querystring_nginx_ok = '(nginx_responsecode:200)'
    querystring_openapi = '(fields.logtype:openapi-access AND NOT httpCode:2*)'
    querystring_openapi_ok = '(fields.logtype:openapi-access AND httpCode:2*)'
    query_nginx = query.Query(querystring_nginx, 'now-10s', 'now').__str__()
    query_nginx_ok = query.Query(querystring_nginx_ok, 'now-10s', 'now').__str__()
    query_openapi = query.Query(querystring_openapi, 'now-10s', 'now').__str__()
    query_openapi_ok = query.Query(querystring_openapi_ok, 'now-10s', 'now').__str__()
    while 1:
        for i in index_list:
            try:
                if 'nginx-proxy' in i:
                    se = Search(i, query_nginx, fields_nginx, client)
                    se_ok = Search(i, query_nginx_ok, fields_nginx, client)
                    data = se.getdata()
                    data_ok = se_ok.getdata()
                    # 非200状态码的统计条数，并设置counter
                    for item in data:
                        # 过滤掉/api/v1/users/userid接口的请求
                        if '/api/v1/users' in item.values()[0]:
                            continue
                        vhost = item.get('nginx_vhost')
                        request = item.get('nginx_request_api')
                        counter = data.count(item)
                        nginxErrorCount.labels(vhost, request).set(counter)
                    # 200状态码的设置其值为0
                    for item in data_ok:
                        # 过滤掉/api/v1/users/userid接口的请求
                        if '/api/v1/users' in item.values()[0]:
                            continue
                        vhost = item.get('nginx_vhost')
                        request = item.get('nginx_request_api')
                        nginxErrorCount.labels(vhost, request).set(0)
                elif 'order-access' in i:
                    se = Search(i, query_openapi, fields_openapi, client)
                    se_ok = Search(i, query_openapi_ok, fields_openapi, client)
                    data = se.getdata()
                    data_ok = se_ok.getdata()
                    # 非200状态码的统计条数，并设置counter
                    for item in data:
                        appId = item.get('appId')
                        url = item.get('url')
                        counter = data.count(item)
                        openapiErrorCount.labels(appId, url).set(counter)
                    # 200状态码的设置其值为0
                    for item in data_ok:
                        appId = item.get('appId')
                        url = item.get('url')
                        openapiErrorCount.labels(appId, url).set(0)
            except StopIteration:
                pass
        time.sleep(10)


if __name__ == '__main__':
    main()

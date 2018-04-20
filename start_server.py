#!/usr/bin/env python
# -*- coding: utf-8 -*-
from logger import Logger
from prometheus_client import start_http_server
from time import sleep
import elasticsearch
from scripts import startor
mylog = Logger(logfile='/tmp/elk_exporter.log', maxbytes=2*1024*1024,
               backupcount=2)


def startserver(client, port, interval):
    """

    :param port: 服务监听端口
    :param interval: 服务检索间隔时间
    :return: 无
    """
    start_http_server(port)
    while 1:
        # set metrics here
        startor.nginx(client)
        sleep(interval)


if __name__ == '__main__':
    es_client = elasticsearch.Elasticsearch(hosts=['10.104.255.201'],
                                            http_auth=('elastic',
                                                       'elastic'), port=9200)
    server_port = 9102
    interval = 5
    startserver(es_client, server_port, interval)


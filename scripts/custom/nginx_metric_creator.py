# -*- coding: utf-8 -*-
from _elasticsearch.query import Query
from _elasticsearch.search import Search
from prometheus_client import REGISTRY
from _prometheus.metrics import NginxMetrics


class NginxMetricCreator(object):
    def __init__(self, index, fields, es_client):
        self.index = index
        self.fields = fields
        self.es_client = es_client

    def create(self):
        query_total = Query().creatquery('message', '(*)',
                                         'now-5s', 'now')
        res_total = Search().getdata(self.index, query_total, self.fields,
                                     self.es_client)
        count_total = res_total.get('count', 0)

        query_200 = Query().creatquery('message', '(nginx_responsecode:200)',
                                       'now-5s', 'now')
        res_200 = Search().getdata(self.index, query_200, self.fields,
                                   self.es_client)
        count_200 = res_200.get('count', 0)

        query_5xx = Query().creatquery('message', '(nginx_responsecode:5*)',
                                       'now-5s', 'now')
        res_5xx = Search().getdata(self.index, query_5xx, self.fields,
                                   self.es_client)
        count_5xx = res_5xx.get('count', 0)

        query_499 = Query().creatquery('message', '(nginx_responsecode:499)',
                                       'now-5s', 'now')
        res_499 = Search().getdata(self.index, query_499, self.fields,
                                   self.es_client)
        count_499 = res_499.get('count', 0)

        nm = NginxMetrics(metric_type='gauge', count_total=count_total,
                          count_200=count_200, count_5xx=count_5xx,
                          count_499=count_499)

        # 该实例只需注册一次即可，重复注册会报ValueError（无检测collector是否已被注册的方法，故直接pass掉）
        try:
            REGISTRY.register(nm)
        except ValueError:
            pass


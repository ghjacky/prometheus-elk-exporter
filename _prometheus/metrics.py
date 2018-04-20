# -*- coding: utf-8 -*-
from prometheus_client import Metric


class Metrics(object):
    instance = None

    # 实现单例模式，每次的metrics为同一个对象
    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = object.__new__(
                cls)
        return cls.instance

    def __init__(self, metric_type):
        self.metrics = dict()
        self.metric_type = metric_type

    # 使用REGISTRY注册，必须实现collect方法
    def collect(self):
        pass


class NginxMetrics(Metrics):
    def __init__(self, metric_type, count_total, count_200, count_5xx,
                 count_499):
        super(NginxMetrics, self).__init__(metric_type)
        self.count_total = count_total
        self.count_200 = count_200
        self.count_5xx = count_5xx
        self.count_499 = count_499

    def collect(self):
        self.metrics['nginx_total'] = Metric('es_nginx_request_total_count',
                                             'Total count of search for the index',
                                             self.metric_type)
        self.metrics['nginx_total'].add_sample('es_nginx_request_total_count',
                                               value=self.count_total,
                                               labels={'search': 'total',
                                                       })
        yield self.metrics['nginx_total']

        self.metrics['nginx_200'] = Metric('es_nginx_request_200_count',
                                           '200 count of search for the index',
                                               self.metric_type)
        self.metrics['nginx_200'].add_sample('es_nginx_request_200_count',
                                             value=self.count_200,
                                             labels={'search': '200'})
        yield self.metrics['nginx_200']

        self.metrics['nginx_5xx'] = Metric('es_nginx_request_5xx_count',
                                           '5xx count of search for the index',
                                               self.metric_type)
        self.metrics['nginx_5xx'].add_sample('es_nginx_request_5xx_count',
                                             value=self.count_5xx,
                                             labels={'search': '5xx'})
        yield self.metrics['nginx_5xx']

        self.metrics['nginx_499'] = Metric('es_nginx_request_499_count',
                                           '499 count of search for the index',
                                               self.metric_type)
        self.metrics['nginx_499'].add_sample('es_nginx_request_499_count',
                                             value=self.count_499,
                                             labels={'search': '499'})
        yield self.metrics['nginx_499']

        


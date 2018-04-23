# -*- coding: utf-8 -*-
from prometheus_client.core import GaugeMetricFamily


class Metrics(object):
    instance = None

    # 实现单例模式，每次的metrics为同一个对象
    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = object.__new__(cls)
        return cls.instance

    def __init__(self):
        self.metrics = dict()

    # 使用REGISTRY注册，必须实现collect方法
    def collect(self):
        pass


class NginxMetrics(Metrics):
    """
    创建responseCode metrics，继承自Metrics。必须实现collect方法，返回相应metrics
    data i.e:   {
                    'a.com': {'count_200': '200', 'count_3xx': '300'},
                    'b.com': {'count_200': '200', 'count_3xx': '300'},
                    'c.com': {'count_200': '200', 'count_3xx': '300'}
                }
    """
    def __init__(self, data):
        super(NginxMetrics, self).__init__()
        self.data = data

    def collect(self):
        """
        创建'es_nginx_request_count'metric，并根据vhost循环add_metric，并设置相应label
        :return:
        """
        self.metrics['nginx'] = GaugeMetricFamily(
            name='es_nginx_request_count',
            documentation='Count of each response code search for the '
                          'Nginx index',
            labels=['res_code', 'vhost']
        )
        for vhost in self.data.keys():
            count_total = self.data.get(vhost).get('count_total')
            count_200 = self.data.get(vhost).get('count_200')
            count_301 = self.data.get(vhost).get('count_301')
            count_302 = self.data.get(vhost).get('count_302')
            count_304 = self.data.get(vhost).get('count_304')
            count_403 = self.data.get(vhost).get('count_403')
            count_404 = self.data.get(vhost).get('count_404')
            count_499 = self.data.get(vhost).get('count_499')
            count_500 = self.data.get(vhost).get('count_500')
            count_502 = self.data.get(vhost).get('count_502')
            count_504 = self.data.get(vhost).get('count_504')
            self.metrics['nginx'].add_metric(
                value=count_total,
                labels=['all', vhost]
            )
            self.metrics['nginx'].add_metric(
                value=count_200,
                labels=['200', vhost]
            )
            self.metrics['nginx'].add_metric(
                value=count_301,
                labels=['301', vhost]
            )
            self.metrics['nginx'].add_metric(
                value=count_302,
                labels=['302', vhost]
            )
            self.metrics['nginx'].add_metric(
                value=count_304,
                labels=['304', vhost]
            )
            self.metrics['nginx'].add_metric(
                value=count_403,
                labels=['403', vhost]
            )
            self.metrics['nginx'].add_metric(
                value=count_404,
                labels=['404', vhost]
            )
            self.metrics['nginx'].add_metric(
                value=count_499,
                labels=['499', vhost]
            )
            self.metrics['nginx'].add_metric(
                value=count_500,
                labels=['500', vhost]
            )
            self.metrics['nginx'].add_metric(
                value=count_502,
                labels=['502', vhost]
            )
            self.metrics['nginx'].add_metric(
                value=count_504,
                labels=['504', vhost]
            )
        yield self.metrics['nginx']



        


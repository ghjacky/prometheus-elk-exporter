# -*- coding: utf-8 -*-
from _elasticsearch.query import Query
from _elasticsearch.search import Search
from prometheus_client import REGISTRY
from _prometheus.metrics import NginxMetrics


class NginxMetricCreator(object):
    """
    从es检索相应数据，统计各字段的值，并创建相应metrics
    """
    def __init__(self, index, fields, es_client):
        self.index = index
        self.fields = fields
        self.es_client = es_client
        self.data = dict()

    def create(self, vhosts):
        """
        根据vhosts在es中检索相应数据（vhost:['total', 200, 301, 302, 304, 403, 404,
        499, 500, 502, 504]）
        调用_prometheus.metrics创建相应metric
        :param vhosts: vhost列表
        :return:
        """
        for vhost in vhosts:
            query_total = Query().creatquery('message',
                                             '(* AND nginx_vhost:' + vhost + ')',
                                             'now-5s', 'now')
            res_total = Search().getdata(self.index, query_total, self.fields,
                                         self.es_client)
            count_total = res_total.get('count', 0)

            query_200 = Query().creatquery('message',
                                           '(nginx_responsecode:200  AND '
                                           'nginx_vhost:' + vhost + ')',
                                           'now-5s', 'now')
            res_200 = Search().getdata(self.index, query_200, self.fields,
                                       self.es_client)
            count_200 = res_200.get('count', 0)

            query_301 = Query().creatquery('message',
                                           '(nginx_responsecode:301  AND '
                                           'nginx_vhost:' + vhost + ')',
                                           'now-5s', 'now')
            res_301 = Search().getdata(self.index, query_301, self.fields,
                                       self.es_client)
            count_301 = res_301.get('count', 0)

            query_302 = Query().creatquery('message',
                                           '(nginx_responsecode:302  AND '
                                           'nginx_vhost:' + vhost + ')',
                                           'now-5s', 'now')
            res_302 = Search().getdata(self.index, query_302, self.fields,
                                       self.es_client)
            count_302 = res_302.get('count', 0)

            query_304 = Query().creatquery('message',
                                           '(nginx_responsecode:304  AND '
                                           'nginx_vhost:' + vhost + ')',
                                           'now-5s', 'now')
            res_304 = Search().getdata(self.index, query_304, self.fields,
                                       self.es_client)
            count_304 = res_304.get('count', 0)

            query_500 = Query().creatquery('message',
                                           '(nginx_responsecode:500 AND '
                                           'nginx_vhost:' + vhost + ')',
                                           'now-5s', 'now')
            res_500 = Search().getdata(self.index, query_500, self.fields,
                                       self.es_client)
            count_500 = res_500.get('count', 0)

            query_502 = Query().creatquery('message',
                                           '(nginx_responsecode:502 AND '
                                           'nginx_vhost:' + vhost + ')',
                                           'now-5s', 'now')
            res_502 = Search().getdata(self.index, query_502, self.fields,
                                       self.es_client)
            count_502 = res_502.get('count', 0)

            query_504 = Query().creatquery('message',
                                           '(nginx_responsecode:504 AND '
                                           'nginx_vhost:' + vhost + ')',
                                           'now-5s', 'now')
            res_504 = Search().getdata(self.index, query_504, self.fields,
                                       self.es_client)
            count_504 = res_504.get('count', 0)

            query_499 = Query().creatquery('message',
                                           '(nginx_responsecode:499 AND '
                                           'nginx_vhost:' + vhost + ')',
                                           'now-5s', 'now')
            res_499 = Search().getdata(self.index, query_499, self.fields,
                                       self.es_client)
            count_499 = res_499.get('count', 0)

            query_404 = Query().creatquery('message',
                                           '(nginx_responsecode:404 AND '
                                           'nginx_vhost:' + vhost + ')',
                                           'now-5s', 'now')
            res_404 = Search().getdata(self.index, query_404, self.fields,
                                       self.es_client)
            count_404 = res_404.get('count', 0)

            query_403 = Query().creatquery('message',
                                           '(nginx_responsecode:403 AND '
                                           'nginx_vhost:' + vhost + ')',
                                           'now-5s', 'now')
            res_403 = Search().getdata(self.index, query_403, self.fields,
                                       self.es_client)
            count_403 = res_403.get('count', 0)

            self.data.update({
                vhost: {
                    'count_total': count_total,
                    'count_200': count_200,
                    'count_301': count_301,
                    'count_302': count_302,
                    'count_304': count_304,
                    'count_403': count_403,
                    'count_404': count_404,
                    'count_499': count_499,
                    'count_500': count_500,
                    'count_502': count_502,
                    'count_504': count_504,
                }
            })

        nm = NginxMetrics(data=self.data)

        # 该实例只需注册一次即可，重复注册会报ValueError（无检测collector是否已被注册的方法，故直接pass掉）
        try:
            REGISTRY.register(nm)
        except ValueError:
            pass


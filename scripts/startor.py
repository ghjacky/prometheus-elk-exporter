# -*- coding: utf-8 -*-

from scripts.custom.nginx_metric_creator import NginxMetricCreator


# 创建nginx相关metrics
def nginx(client):
    nmc = NginxMetricCreator(index='*-nginx-proxy-*',
                             fields=['nginx_vhost',
                                     'nginx_request_api',
                                     'nginx_responsecode',
                                     'nginx_total_request_time',
                                     'backend_server'
                                     ],
                             es_client=client)
    nmc.create(['api.xdjl.megvii.com',
                'passport.xdjl.megvii.com',
                'openapi.xiaodaijl.com'
                ])







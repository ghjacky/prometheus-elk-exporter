# -*- coding: utf-8 -*-
from elasticsearch.exceptions import ConnectionTimeout
from logger import mylog


class Search(object):
    """
    解析检索出的数据，仅保留指定的字段
    """
    def __init__(self):
        self.res = []

    def getdata(self, index, query, fields, client):
        try:
            data = client.search(index=index, size=100, body=query)
            count = data['hits']['total']
            data = data['hits']['hits']
        except ConnectionTimeout:
            mylog.warning('Es连接失败！')
            count = -1
            data = []
        for d in data:
            item = {}
            for f in fields:
                item.update({
                    f: d.get('_source').get(f)
                })
            self.res.append(item)
        print({'data': self.res, 'count': count})
        return {'data': self.res, 'count': count}




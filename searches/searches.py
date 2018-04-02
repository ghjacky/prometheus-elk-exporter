# -*- coding: utf-8 -*-


class Search(object):
    def __init__(self, index, query, fields, client):
        self.index = index
        self.client = client
        self.query = query
        self.fields = fields

    def getdata(self):
        res = []
        data = self.client.search(index=self.index, size=100, body=self.query)
        data = data['hits']['hits']
        for d in data:
            item = {}
            for f in self.fields:
                item.update({
                    f: d.get('_source').get(f)
                })
            res.append(item)
        return res

# -*- coding: utf-8 -*-
import _elasticsearch


class Query(object):
    def __init__(self, ):
        pass

    def __query(self, field, querystring, starttime, endtime):
        qstring = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "query_string": {
                                "default_field": field,
                                "query": querystring
                            }
                        },
                        {
                            "range": {
                                "@timestamp": {
                                    "gte": starttime,
                                    "lte": endtime,
                                }
                            }
                        },
                    ]
                }
            }
        }
        return qstring

    def creatquery(self, field, querystring, starttime, endtime):
        return self.__query(field, querystring, starttime, endtime)


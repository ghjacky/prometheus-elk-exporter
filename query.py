# -*- coding: utf-8 -*-
import elasticsearch


class Query(object):
    def __init__(self, querystring, starttime, endtime):
        self.querystring = querystring
        self.starttime = starttime
        self.endtime = endtime

    def __str__(self):
        qstring = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "query_string": {
                                "default_field": "message",
                                "query": self.querystring
                            }
                        },
                        {
                            "range": {
                                "@timestamp": {
                                    "gte": self.starttime,
                                    "lte": self.endtime,
                                }
                            }
                        },
                    ]
                }
            }
        }
        return qstring

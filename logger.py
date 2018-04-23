# -*- coding: utf-8 -*-
import logging
from logging.handlers import RotatingFileHandler


# 定义日志输出
class Logger(object):
    def __init__(self, logfile='/var/log/elk_exporter.log',
                 maxbytes=5*1024*1024, backupcount=2):
        self.logfile = logfile
        self.logformater = logging.Formatter('%(asctime)s [%(levelname)s] %('
                                         'funcName)s(%(lineno)d) %(message)s')
        self.loghandler = RotatingFileHandler(filename=logfile, mode='a',
                                              maxBytes=maxbytes,
                                              backupCount=backupcount)
        self.loghandler.setFormatter(self.logformater)
        self.__mylog = logging.getLogger('root')
        self.__mylog.setLevel(logging.DEBUG)
        self.__mylog.addHandler(self.loghandler)

    def getlogger(self):
        return self.__mylog


mylog = Logger(logfile='/tmp/elk_exporter.log', maxbytes=2*1024*1024,
               backupcount=2).getlogger()
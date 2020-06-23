# -*- coding: utf-8 -*- 
import datetime

def test():
    pass

def logPrint(logLevel, logStr):
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    print(now_time + ' ' +logLevel + ' ' + logStr)
    

def logW(logStr):
    logPrint('WARN :', logStr)

def logE(logStr):
    logPrint('ERROR:', logStr)

def logI(logStr):
    logPrint('INFO :', logStr)

def logD(logStr):
    logPrint('DEBUG:', logStr)

if __name__ == "__main__":
    logE("TEST")
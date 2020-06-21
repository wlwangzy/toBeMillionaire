# -*- coding: utf-8 -*- 
import requests
import sys
from py_data import *
reload(sys)
sys.setdefaultencoding('utf8')

if __name__ == "__main__":
    requestUrl = 'http://zq.win007.com/analysis/1743046sb.htm#porlet_0'
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
    html = requests.get(requestUrl, headers = header)
    html.encoding = 'utf-8'
    #print html.text
    classHistroyGameData, classInGameData1, classInGameData2 = praseHtmlGameTableData(html.text)
    classIntegralData = praseHtmlIntegralData(html.text)

    requestUrl2 = 'http://zq.win007.com/analysis/odds/1743046.htm?' + str(int(time.time()) * 1000)

    header2 = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36',
                'Referer':'http://zq.win007.com/analysis/1743046sb.htm'}
    html = requests.get(requestUrl2, headers = header2)
    html.encoding = 'utf-8'

    #print html.text
    classIndexData = praseHtmlIndexData(html.text)
    
    writeExcelData(classHistroyGameData, classInGameData1, classInGameData2, classIndexData, classIntegralData)
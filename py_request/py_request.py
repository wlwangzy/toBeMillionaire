# -*- coding: utf-8 -*- 
import requests
import sys
from py_data import *
from INCLUDE import *
if sys.version_info.major == 2:
    reload(sys)
    sys.setdefaultencoding('utf8')

def requstUrl(requestId, outPathFile):
    requestUrl = 'http://zq.win007.com/analysis/' + requestId + 'sb.htm#porlet_0'
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
    html = requests.get(requestUrl, headers = header)
    html.encoding = 'utf-8'
    #print html.text
    classHistroyGameData, classInGameData1, classInGameData2 = praseHtmlGameTableData(html.text)
    classIntegralData = praseHtmlIntegralData(html.text)

    requestUrl2 = 'http://zq.win007.com/analysis/odds/' + requestId + '.htm?' + str(int(time.time()) * 1000)

    header2 = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36',
                'Referer':'http://zq.win007.com/analysis/' + requestId + 'sb.htm'}
    html = requests.get(requestUrl2, headers = header2)
    html.encoding = 'gb2312'

    #print html.text
    classIndexData = praseHtmlIndexData(html.text)
    
    allGameData = writeExcelData(outPathFile, classHistroyGameData, classInGameData1, classInGameData2, classIndexData, classIntegralData)

    logI("write excel success")

    return allGameData

def decodeUrl(sUrl):
    sUrls = sUrl.split("sb")
    strLogE = "the url is error: " + sUrl
    if len(sUrls) is 1:
        return False, strLogE
    sUrlss = sUrls[0].split("/")

    if len(sUrlss) is 1:
        return False, strLogE

    logI("url is %s " % sUrlss[-1])

    return sUrlss[-1], ""

def toGetRquest(sUrl):
    requestId, errorData = decodeUrl(sUrl) 
    if requestId is False:
        return False, errorData

    basedir = os.path.abspath(os.path.dirname(__file__))

    outPutdir = basedir + "/web/output/" + datetime.datetime.now().strftime('%Y-%m-%d')
    if not os.path.exists(outPutdir):
        os.makedirs(outPutdir)
    outPutFile = outPutdir + "/" + requestId + ".xls"
     
    logI("write to file path : " + outPutFile)

    iTime = 0
    allGameData = {}
    try:
        allGameData = requstUrl(requestId, outPutFile)
    except Exception as e:
        logW(str(e))
        while iTime < 5:
            try:
                allGameData = requstUrl(requestId, outPutFile)
            except Exception as e:
                logW(str(e))
            else:
                break
            finally:
                iTime += 1

    if iTime == 3:
        return False, "request timeout"
    
    dicData = {}
    dicData["outPutFile"] = datetime.datetime.now().strftime('%Y-%m-%d') + "/" + requestId + ".xls"
    dicData["allGameData"] = allGameData
    #print allGameData
    return True, dicData



if __name__ == "__main__":
    #toGetRquest("http://zq.win007.com/analysis/1743046sb.htm#porlet_0")
    sUrl = "http://zq.win007.com/analysis/1743046sb.htm#porlet_0"

    requestId, errorData = decodeUrl(sUrl) 

    basedir = os.path.abspath(os.path.dirname(__file__))

    outPutdir = basedir + "/web/output/" + datetime.datetime.now().strftime('%Y-%m-%d')
    if not os.path.exists(outPutdir):
        os.makedirs(outPutdir)
    outPutFile = outPutdir + "/" + requestId + ".xls"
     
    logI("write to file path : " + outPutFile)
    
    #allGameData = requstUrl(requestId, outPutFile)
    

    requestUrl2 = 'http://vip.win007.com/changeDetail/handicap.aspx?id=1868527&companyid=1&l=0'

    header2 = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36',
                'Referer':'http://zq.win007.com/analysis/' + requestId + 'sb.htm'}
    html = requests.get(requestUrl2, headers = header2)
    html.encoding = 'gb2312'

    #print html.text

    praseHtmlNowData(html.text)
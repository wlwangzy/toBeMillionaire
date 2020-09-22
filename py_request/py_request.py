# -*- coding: utf-8 -*- 
from selenium import webdriver
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

    # 对赛往绩、主队战绩、客队战绩
    classHistroyGameData, classInGameData1, classInGameData2 = praseHtmlGameTableData(html.text)

    # 联赛积分排名
    classIntegralData = praseHtmlIntegralData(html.text)

    requestUrl2 = 'http://zq.win007.com/analysis/odds/' + requestId + '.htm?' + str(int(time.time()) * 1000)

    header2 = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36',
                'Referer':'http://zq.win007.com/analysis/' + requestId + 'sb.htm'}
    html = requests.get(requestUrl2, headers = header2)
    html.encoding = 'utf-8'

    #print html.text
    # 即时指数比较
    classIndexData = praseHtmlIndexData(html.text)
    
    allGameData = None
    if outPathFile is not None:
        allGameData = writeExcelData(outPathFile, classHistroyGameData, classInGameData1, classInGameData2, classIndexData, classIntegralData)
        logI("write excel success")
    else:
        encodeToCData(classIntegralData,classHistroyGameData,classInGameData1,classInGameData2,classIndexData)
        return classIntegralData
        pass

    return allGameData

def decodeUrl(sUrl):
    sUrls = sUrl.split("sb")
    strLogE = "the url is error: " + sUrl
    if len(sUrls) == 1:
        return False, strLogE
    sUrlss = sUrls[0].split("/")

    if len(sUrlss) == 1:
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

def toGetRquestNoExcel(sUrl):
    requestId, errorData = decodeUrl(sUrl) 
    if requestId is False:
        return False, errorData

    iTime = 0
    allGameData = {}
    #allGameData = requstUrl(requestId, None)

    try:
        allGameData = requstUrl(requestId, None)
    except Exception as e:
        logW(str(e))
        while iTime < 5:
            try:
                allGameData = requstUrl(requestId, None)
            except Exception as e:
                logW(str(e))
            else:
                break
            finally:
                iTime += 1

    if iTime == 3:
        return False, "request timeout"

    print(allGameData)
    #for sNode in allGameData:
    #    print(sNode)

    return True

def getIdList():

    # 目标网页URL
    url = "http://live.win007.com/"
    
    # 目标Tag : 数据table（id = 'table_live'）中的<tr>
    trTagPath = "//table[@id='table_live']/tbody/tr"
    
    # 生成Web终端，并访问目标网页URL
    driver = webdriver.Chrome()
    driver.minimize_window()
    driver.implicitly_wait(3)
    driver.get(url)

    print("")
    print("processing ...")
    print("")

    # 解析网页标签
    trTagList = driver.find_elements_by_xpath(trTagPath)
    idList = []

    for trTag in trTagList:
        if trTag.is_displayed() and ("tr1_" == trTag.get_attribute("id")[0:4]) :
            idList.append(trTag.get_attribute("id")[4:])
    
    # 关闭Web终端
    driver.close()
    
    print("")
    print("process over!")
    print("")
    
    # 返回结果
    return idList

if __name__ == "__main__":
    
    retList = getIdList()

    print("===========")
    for id in retList:
        print(id)

    print("-----------")
    print(len(retList))
    print("===========")
    
    for id in retList:
        url = "http://zq.win007.com/analysis/" + id + "sb.htm"
        toGetRquestNoExcel(url)
    
    #url = "http://zq.win007.com/analysis/" + retList[0] + "sb.htm"
    #url = "http://zq.win007.com/analysis/1879934sb.htm"
    #toGetRquestNoExcel(url)

    '''
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
    '''
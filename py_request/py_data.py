# -*- coding: utf-8 -*- 

import sys
import re
from INCLUDE import *

class H0V0Data:
    def __init__(self):
        self.sPraseH0V0DIC = {}
        #self.setDataH0V0(sPraseDataH0List, sPraseDataV0List)

    def setDataH0V0(self, sPraseDataH0List , sPraseDataV0List):
        for nodeH0 in sPraseDataH0List:
            nodeDic = {}
            nodeH0s = nodeH0.split(',')
            nodeDic[nodeH0s[1]] = nodeH0s[2:]
            if nodeH0s[0] not in self.sPraseH0V0DIC.keys():
                self.sPraseH0V0DIC[nodeH0s[0]] = []
            
            self.sPraseH0V0DIC[nodeH0s[0]].append(nodeDic)

        for nodeV0 in sPraseDataV0List:
            nodeDic = {}
            nodeV0s = nodeV0.split(',')
            nodeDic[nodeV0s[1]] = nodeV0s[2:]
            if nodeV0s[0] not in self.sPraseH0V0DIC.keys():
                self.sPraseH0V0DIC[nodeV0s[0]] = []
            
            self.sPraseH0V0DIC[nodeV0s[0]].append(nodeDic)
    
        #print(self.sPraseH0V0DIC)

    def findDatH0V0(self, liGameId, iTypeId, iPos):
        if liGameId in self.sPraseH0V0DIC.keys():
            #print self.sPraseH0V0DIC[liGameId]
            for node in self.sPraseH0V0DIC[liGameId]:
                if str(iTypeId) in node.keys():
                    sTmp = node[str(iTypeId)][iPos]
                    sTmps = sTmp.split('\'')
                    if len(sTmps) > 0:
                        sTmp = sTmps[1]
  
                    return sTmp
            else:
                #node  = self.sPraseH0V0DIC[liGameId]
                #print node[0]
                return ''
        else:
            return ''


class gameData:
    def __init__(self, H0V0Data):
        self.iCount = 0             #列表数量
        self.iGameId = []            #id 用于查找数据
        self.sGameType = []         #类型
        self.sGameDate = []         #日期
        self.sGameHomeField = []    #主场
        self.sCore = []             #比分
        self.sCorner = []           #角球
        self.sAwayGroun = []        #客场
        self.fDataMap1 = []         #初盘 终盘 前数据
        self.fDataMap2 = []         #初盘 终盘 后数据
        #self.fDataMain1 = {'皇冠':[], '澳门':[], 'Bet365':[], '易胜博':[], '12Bet':[]}   #主
        #self.fDataTap = {'皇冠':[], '澳门':[], 'Bet365':[], '易胜博':[], '12Bet':[]}  #盘口
        #self.fDataGuest1 = {'皇冠':[], '澳门':[], 'Bet365':[], '易胜博':[], '12Bet':[]}   #客
        #self.fDataMain2 = {'皇冠':[], '澳门':[], 'Bet365':[], '易胜博':[], '12Bet':[]}   #主
        #self.fDataAnd = {'皇冠':[], '澳门':[], 'Bet365':[], '易胜博':[], '12Bet':[]}   #和
        #self.fDataGuest2 = {'皇冠':[], '澳门':[], 'Bet365':[], '易胜博':[], '12Bet':[]}   #客
        self.H0V0Data = H0V0Data


        # self.vData = '' #历史战绩表格数据
        # self.aData = ''
        # self.h2ata = ''
        # self.a2ata = ''
        # self.h0Data = '' #值查找表
        # self.v0Data = '' #值查找表

    #解析初终盘的数据
    def decodeListToDic(self, iFindId, iFindType):
        dicData = {}
        dicDataNodeStart = []
        dicDataNodeEnd = []
        dicDataNodeStart.append(self.H0V0Data.findDatH0V0(iFindId, iFindType, 0))
        dicDataNodeStart.append(self.H0V0Data.findDatH0V0(iFindId, iFindType, 1))
        dicDataNodeStart.append(self.H0V0Data.findDatH0V0(iFindId, iFindType, 2))
        dicDataNodeEnd.append(self.H0V0Data.findDatH0V0(iFindId, iFindType, 3))
        dicDataNodeEnd.append(self.H0V0Data.findDatH0V0(iFindId, iFindType, 4))
        dicDataNodeEnd.append(self.H0V0Data.findDatH0V0(iFindId, iFindType, 5))
        dicData["start"] = dicDataNodeStart
        dicData["end"] = dicDataNodeEnd

        return dicData
            

    def setData(self, sPraseData):
        sNodeList = sPraseData.split(',')
        #i = 0
        #for node2 in sNodeList:
            #print(str(i) + " : " + node2)
        #    i += 1
        self.iGameId.append(sNodeList[15])
        self.sGameType.append(sNodeList[2].split('\'')[1])
        self.sGameDate.append(sNodeList[0].split('\'')[1])
        try:
            sNodeLists = sNodeList[5].split('</span>')
            if len(sNodeLists) > 2:
                self.sGameHomeField.append(sNodeLists[-2])
            else:
                self.sGameHomeField.append(sNodeLists[-2].split('>')[1])
        except Exception, e:
            logE(str(e) + 'sAwayGroun = ' + sNodeList[5])
            self.sGameHomeField.append(sNodeList[5])
        
        self.sCore.append(sNodeList[8] + '-' + sNodeList[9] + '(' + sNodeList[10].split('\'')[1] + ')')
        self.sCorner.append(sNodeList[16].split('\'')[1] + '-' + sNodeList[17].split('\'')[1])
        try:
            self.sAwayGroun.append(sNodeList[7].split('>')[1].split('<')[0])
        except Exception, e:
            logE(str(e) + 'sAwayGroun = ' + sNodeList[7])
            self.sGameHomeField.append(sNodeList[7])
        #print("ddd " + sNodeList[15])
        dicData1 = {}
        dicData1["澳门"] = self.decodeListToDic(sNodeList[15], 1)
        dicData1["皇冠"] = self.decodeListToDic(sNodeList[15], 3)
        dicData1["Bet365"] = self.decodeListToDic(sNodeList[15], 8)
        dicData1["易胜博"] = self.decodeListToDic(sNodeList[15], 12)
        dicData1["12bet"] = self.decodeListToDic(sNodeList[15], 24)
        self.fDataMap1.append(dicData1)

        dicData2 = {}
        dicData2["平均欧赔"] = self.decodeListToDic(sNodeList[15], 0)
        dicData2["12bet"] = self.decodeListToDic(sNodeList[15], 18)
        dicData2["澳门"] = self.decodeListToDic(sNodeList[15], 80)
        dicData2["威廉希尔"] = self.decodeListToDic(sNodeList[15], 115)
        dicData2["bet365"] = self.decodeListToDic(sNodeList[15], 281)
        dicData2["皇冠"] = self.decodeListToDic(sNodeList[15], 545)
        self.fDataMap2.append(dicData2)

        self.iCount += 1

    def writeToExcel(self):
        pass

    def outputData(self):
        i = 0
        while i < self.iCount:
            print "==============="
            print self.sGameType[i]
            print self.sGameDate[i]
            print self.sGameHomeField[i]
            print self.sCore[i]
            print self.sCorner[i]
            print self.sAwayGroun[i]
            print "data :"
            print self.fDataMap1
            print self.fDataMap2
            print "================"
            i += 1
        print self.iCount
        print i

#即时指数数据
class indexData:
    def __init__(self):
         self.indexDataList = []

    def decodeIndexData(self, nowIndexData):
        #print nowIndexData
        nowIndexDatas = nowIndexData.split('^')
        self.indexDataList = []
        for node in nowIndexDatas:
            indexDataListNode = {}
            nodes = node.split(';')
            nodeData1 = nodes[2].split(',')#初盘 欧洲指数，欧转亚盘 实际最新亚盘 大小球
            nodeData2 = nodes[3].split(',')#终盘 欧洲指数，欧转亚盘 实际最新亚盘 大小球
            nodeData3 = nodes[4].split(',')#滚球 欧洲指数，欧转亚盘 实际最新亚盘 大小球
            indexDataListNode[nodes[1]] = []
            indexDataListNode[nodes[1]].append(nodeData1)
            indexDataListNode[nodes[1]].append(nodeData2)
            indexDataListNode[nodes[1]].append(nodeData3)
            self.indexDataList.append(indexDataListNode)
        
    def outputData(self):
        for node in self.indexDataList:
            print node
        print "index number = " + str(len(self.indexDataList))

#联赛积分排名
class integralData:
    def __init__(self, sLeftTableName, sRightTableName):
        self.sLeftTableName = sLeftTableName
        self.sRightTableName = sRightTableName
        self.integralDataList = {}

    def decodeIntefralData(self, listIntegralData):
        i = 0
        self.integralDataList = {}
        self.integralDataList["全场"] = []
        self.integralDataList["半场"] = []
        localDataDic = {}

        for node in listIntegralData[:16]:
            findData = '<td.*?>(.*?)</td>'
            tmpData = re.findall(findData, node, re.S)
            #tmpData = node.split('</td>\r\n')
            nodeDic = {}
            tmpDatas = re.findall('>(.*?)<', tmpData[0], re.S)
            if len(tmpDatas) > 0:
                tmpData[0] = tmpDatas[0]
            nodeDic[tmpData[0]] = []
            for tmpDataNode in tmpData[1:]:
                nodeDic[tmpData[0]].append(tmpDataNode)
            if i < 8:
                self.integralDataList["全场"].append(nodeDic)
            else:
                self.integralDataList["半场"].append(nodeDic)
            i += 1
    
    def outputData(self):
        print self.integralDataList

def praseData(sStr):
    sStrList = sStr.split('],[')
    #print(len(sStrList))
    for node in sStrList:
        #print("test : " + node)
        pass

    return sStrList

#解析历史战绩表格
def praseDataOld(classOldGameData, sStrList):
    for node in sStrList:
        #print("test : " + node)
        classOldGameData.setData(node)

#解析对应数据表格
def praseDataH0V0(classH0V0Data, sStrListH0, sStrListV0):
    classH0V0Data.setDataH0V0(sStrListH0, sStrListV0)

def praseHtmlGameTableData(sHtmlData):
    findVdata  = 'var v_data = (.*?);'
    findhdata  = 'var h_data=(.*?);'
    findadata  = 'var a_data = (.*?);'
    findh2data  = 'var h2_data=(.*?);'
    finda2data  = 'var a2_data = (.*?);'
    findaVsH0data  = 'var Vs_hOdds=(.*?);'
    findaVsV0data  = 'var Vs_eOdds = (.*?);'
    
    tmpData = re.findall(findVdata, sHtmlData , re.S)
    vData = tmpData[0]
    tmpData = re.findall(findhdata, sHtmlData , re.S)
    hData = tmpData[0]
    tmpData = re.findall(findadata, sHtmlData , re.S)
    aData = tmpData[0]
    tmpData = re.findall(findh2data, sHtmlData , re.S)
    h2ata = tmpData[0]
    tmpData = re.findall(finda2data, sHtmlData , re.S)
    a2ata = tmpData[0]
    tmpData = re.findall(findaVsH0data, sHtmlData , re.S)
    h0Data = tmpData[0]
    tmpData = re.findall(findaVsV0data, sHtmlData , re.S)
    v0Data = tmpData[0]
    
    #初始化数据表格
    classH0V0Data = H0V0Data()
    praseDataH0V0(classH0V0Data, praseData(h0Data[2:-2]), praseData(v0Data[2:-2]))

    #初始化历史战绩
    classHistroyGameData = gameData(classH0V0Data)
    praseDataOld(classHistroyGameData, praseData(vData[2:]))
    #classHistroyGameData.outputData()
    #近期数据1
    classInGameData1 = gameData(classH0V0Data)
    praseDataOld(classInGameData1, praseData(hData[2:]))
    #classInGameData1.outputData()
    #近期数据2
    classInGameData2 = gameData(classH0V0Data)
    praseDataOld(classInGameData2, praseData(aData[2:]))
    #classInGameData2.outputData()

    return classHistroyGameData, classInGameData1, classInGameData2

#解析即时指数
def praseHtmlIndexData(sHtmlData):
    findIndexNow = '<input type=\'hidden\' value=\'(.*?)\''
    
    tmpData = re.findall(findIndexNow, sHtmlData , re.S)
    nowIndexData = tmpData[0]

    classIndexData = indexData()
    classIndexData.decodeIndexData(nowIndexData)

    return classIndexData

#解析联赛积分
def praseHtmlIntegralData(sHtmlData):
    #print sHtmlData

    findIIntegral= '<tr align=middle bgcolor=.*?>(.*?)</tr>'
    tmpData = re.findall(findIIntegral, sHtmlData, re.S)
    
    #for node in tmpData:
    #    print node
    sTableName = re.findall('<font class=vander16 style="color:#000"><b>(.*?)</b>', sHtmlData, re.S)

    classIntegralData = integralData(sTableName[0], sTableName[1])
    classIntegralData.decodeIntefralData(tmpData)
    #classIntegralData.outputData()

    return classIntegralData


if __name__ == "__main__":
    #test source data http://zq.win007.com/analysis/1743046sb.htm
     #初始化数据表格
    classH0V0Data = H0V0Data()
    praseDataH0V0(classH0V0Data, praseData(t2[2:-2]), praseData(t3[2:-2]))

    #初始化历史战绩
    classOldGameData = gameData(classH0V0Data)
    praseDataOld(classOldGameData, praseData(t1[2:]))

    classOldGameData.outputData()



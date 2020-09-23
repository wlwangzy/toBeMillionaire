# -*- coding: utf-8 -*- 

import sys
import re
import json
import platform
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
        self.iGameId = []           #id 用于查找数据
        self.sGameType = []         #类型
        self.sGameDate = []         #日期
        self.sGameHomeField = []    #主场
        self.sCore = []             #比分
        self.sCorner = []           #角球
        self.sAwayGroun = []        #客场
        self.fDataMap1 = []         #初盘 终盘 前数据
        self.fDataMap2 = []         #初盘 终盘 后数据
        self.sGameResult = []       #胜负结果
        self.sWinCnt = 0            #胜场次统计
        self.sDrawCnt = 0           #平场次统计
        self.sLoseCnt = 0           #负场次统计
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
        if self.iCount >= 10:
            return

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
        except Exception as e:
            logD(str(e) + ' sAwayGroun = ' + sNodeList[5])
            self.sGameHomeField.append(sNodeList[5])
        
        self.sCore.append(sNodeList[8] + '-' + sNodeList[9] + '(' + sNodeList[10].split('\'')[1] + ')')
        self.sCorner.append(sNodeList[16].split('\'')[1] + '-' + sNodeList[17].split('\'')[1])
        try:
            self.sAwayGroun.append(sNodeList[7].split('>')[1].split('<')[0])
        except Exception as e:
            logD(str(e) + ' sAwayGroun = ' + sNodeList[7])
            self.sAwayGroun.append(sNodeList[7])

        if int(sNodeList[12]) < 0:
            sTmpData = '负'
            self.sLoseCnt += 1
        elif int(sNodeList[12]) > 0:
            sTmpData = '胜'
            self.sWinCnt += 1
        else:
            sTmpData = '平'
            self.sDrawCnt += 1
        self.sGameResult.append(sTmpData)
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
        if self.iCount > 10:
            gameCnt = 10
        else:
            gameCnt = self.iCount
        i = 0
        while i < gameCnt:
            print("========game",i)
            print(self.sGameType[i])
            print(self.sGameDate[i])
            print(self.sGameHomeField[i])
            print(self.sCore[i])
            print(self.sCorner[i])
            print(self.sAwayGroun[i])
            print(self.sGameResult[i])
            #print(self.fDataMap1)
            #print(self.fDataMap2)
            print("================")
            i += 1
        print("共计数",self.iCount)
        print("胜",self.sWinCnt)
        print("平",self.sDrawCnt)
        print("负",self.sLoseCnt)
        #print(i)

#即时指数数据
class indexData:
    def __init__(self):
         self.indexDataList = []

    def decodeIndexData(self, nowIndexData):
        #print(nowIndexData)
        nowIndexDatas = nowIndexData.split('^')
        self.indexDataList = []
        for node in nowIndexDatas:
            indexDataListNode = {}
            nodes = node.split(';')
            nodeData1 = nodes[2].split(',')#初盘 欧洲指数，欧转亚盘 实际最新亚盘 大小球
            nodeData2 = nodes[3].split(',')#终盘 欧洲指数，欧转亚盘 实际最新亚盘 大小球
            #nodeData3 = nodes[4].split(',')#滚球 欧洲指数，欧转亚盘 实际最新亚盘 大小球
            indexDataListNode[nodes[1]] = []
            indexDataListNode[nodes[1]].append(nodeData1)
            indexDataListNode[nodes[1]].append(nodeData2)
            #indexDataListNode[nodes[1]].append(nodeData3)
            self.indexDataList.append(indexDataListNode)
        
    def outputData(self):
        for node in self.indexDataList:
            print(node)
        print("index number = " + str(len(self.indexDataList)))

        #with open('D:\\python\\aa.txt','a',encoding='utf-8') as file_handle:   # .txt可以不自己新建,代码会自动新建
        #    file_handle.write("{}\n".format(self.indexDataList))

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
        print(self.integralDataList)

class nowTimeData:
    def __init__(self):
        self.nowData = []
        self.nowDataAll = []

    def decodeNowTimeData(self, listNowData, listNowDataAll):
        i = 0
        while (i < len(listNowData) - 2 and "FONT" not in listNowData[i]):
            tmpDic = {}
            tmpDic["iTime"] = listNowData[i]
            tmpDic["sPan"] = listNowData[i + 1]
            tmpDic["iData"] = listNowData[i + 2].split("&nbsp;")[-1]

            if "<" in tmpDic["iData"]:
                tmpDic["iData"] = tmpDic["iData"].split("<")[0]

            self.nowData.append(tmpDic)
            i += 3

        
        for node in listNowDataAll:
            findTmp2= '>(.*?)</TD>'
            tmpData = re.findall(findTmp2, node, re.S)
            # print tmpData
            tmpData = self.praseData(tmpData)
            self.nowDataAll.append(tmpData)
    
    def praseData(self, sData):
        i = 0
        while i < len(sData):
            findTmp= '>(.*?)<'
            tmpData = re.findall(findTmp, sData[i], re.S)
            if len(tmpData) != 0:
                for node in tmpData:
                    if node != '':
                        sData[i] = node
                        break
            else:
                if "FONT" in sData[i]:
                    sData[i] = sData[i].split('>')[-1]

            i += 1


        return sData

    def outputData(self):
        #print "nowData"
        for node in self.nowData:
            print(node)

        #print "nowData All"
        for node in self.nowDataAll:
            print(node)

        
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
        if node == '' or node == None:
            return None
        else:
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

   # print(sHtmlData)
    
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
    findTmp = '<input type=\'hidden\' value=\'(.*?)\''
    
    tmpData = re.findall(findTmp, sHtmlData , re.S)
    nowIndexData = tmpData[0]

    classIndexData = indexData()
    classIndexData.decodeIndexData(nowIndexData)
    #classIndexData.outputData()

    return classIndexData

#解析联赛积分
def praseHtmlIntegralData(sHtmlData):
    #print(sHtmlData)

    findTmp= '<tr align=middle bgcolor=.*?>(.*?)</tr>'
    tmpData = re.findall(findTmp, sHtmlData, re.S)
    #print(sHtmlData)
    #for node in tmpData:
    #    print(node)
    sTableName = re.findall('<font class=vander16 style="color:#000"><b>(.*?)</b>', sHtmlData, re.S)

    classIntegralData = integralData(sTableName[0], sTableName[1])
    classIntegralData.decodeIntefralData(tmpData)
    #classIntegralData.outputData()

    return classIntegralData

#解析实时数据
def praseHtmlNowData(sHtmlData):
    findTmp= '<TD.*?>(.*?)</TD>'
    tmpData = re.findall(findTmp, sHtmlData, re.S)

    findTmp2= '<TR align=center.*?>(.*?)</TR>'
    tmpData2= re.findall(findTmp2, sHtmlData, re.S)
    #for node in tmpData:
     #   print node


    classNowData = nowTimeData()
    classNowData.decodeNowTimeData(tmpData, tmpData2)
    #classNowData.outputData()

def encodeToCData(gameId,classIntegralData,classHistroyGameData,classInGameData1,classInGameData2,classIndexData):
    dicData = {}

    dicData["gameId"] = gameId
    dicData["bNeutral"] = 0 #是否为中立 未赋值 默认给中立
    dicData["cType"] = "zc" #中超 中甲 等等
    dicData["iQdsa"] = 0

    if "全场" in classIntegralData.integralDataList.keys():
        dicData["iHomeRank"] = int(classIntegralData.integralDataList["全场"][0]["总"][8]) #主队排名
        dicData["iHomeRecentWin"] = int(classInGameData1.sWinCnt) #classIntegralData.integralDataList["全场"][0]["总"][1] #主队近期战绩胜场次
        dicData["iHomeRecentDraws"] = int(classInGameData1.sDrawCnt) #classIntegralData.integralDataList["全场"][0]["总"][2] #主队近期战绩平场次
        dicData["iHomeRecentLose"] = int(classInGameData1.sLoseCnt) #classIntegralData.integralDataList["全场"][0]["总"][3] #主队近期战绩负场次
    
        #用的联赛主场战绩
        dicData["iHomeRecentHomeWin"] = int(classIntegralData.integralDataList["全场"][1]["主"][1]) #主队近期战绩主场胜场次
        dicData["iHomeRecentHomeDraws"] = int(classIntegralData.integralDataList["全场"][1]["主"][2]) #主队近期战绩主场平场次
        dicData["iHomeRecentHomeLose"] = int(classIntegralData.integralDataList["全场"][1]["主"][2]) #主队近期战绩主场负场次

        dicData["iAwayRank"] = int(classIntegralData.integralDataList["全场"][4]["总"][8]) #客队排名
        dicData["iAwayRecentWin"] = int(classInGameData2.sWinCnt) #classIntegralData.integralDataList["全场"][4]["总"][1] #客队近期战绩胜场次
        dicData["iAwayRecentDraws"] = int(classInGameData2.sDrawCnt) #classIntegralData.integralDataList["全场"][4]["总"][2] #客队近期战绩平场次
        dicData["iAwayRecentLose"] = int(classInGameData2.sLoseCnt) #classIntegralData.integralDataList["全场"][4]["总"][3] #客队近期战绩负场次
    
        #用的联赛主场战绩
        dicData["iAwayRecentAwayWin"] = int(classIntegralData.integralDataList["全场"][6]["客"][1]) #客队近期战绩客场胜场次
        dicData["iAwayRecentAwayDraws"] = int(classIntegralData.integralDataList["全场"][6]["客"][2]) #客队近期战绩客场平场次
        dicData["iAwayRecentAwayLose"] = int(classIntegralData.integralDataList["全场"][6]["客"][2]) #客队近期战绩客场负场次
    
    dicData["iVsRecHomeWin"] = int(classHistroyGameData.sWinCnt) # 对赛往绩主队胜场次
    dicData["iVsRecHomeDraws"] = int(classHistroyGameData.sDrawCnt) # 对赛往绩主队平场次
    dicData["iVsRecHomeLose"] = int(classHistroyGameData.sLoseCnt) # 对赛往绩主队负场次

#var GoalCn = "平手,平/半,半球,半/一,一球,一/球半,球半,球半/两,两球,两/两球半,两球半,两球半/三,三球,三/三球半,三球半,三球半/四球,四球,四/四球半,四球半,四球半/五,五球,五/五球半,五球半,五球半/六,六球,六/六球半,六球半,六球半/七,七球,七/七球半,七球半,七球半/八,八球,八/八球半,八球半,八球半/九,九球,九/九球半,九球半,九球半/十,十球".split(",");
#var GoalCn2 = ["0", "0/0.5", "0.5", "0.5/1", "1", "1/1.5", "1.5", "1.5/2", "2", "2/2.5", "2.5", "2.5/3", "3", "3/3.5", "3.5", "3.5/4", "4", "4/4.5", "4.5", "4.5/5", "5", "5/5.5", "5.5", "5.5/6", "6", "6/6.5", "6.5", "6.5/7", "7", "7/7.5", "7.5", "7.5/8", "8", "8/8.5", "8.5", "8.5/9", "9", "9/9.5", "9.5", "9.5/10", "10", "10/10.5", "10.5", "10.5/11", "11", "11/11.5", "11.5", "11.5/12", "12", "12/12.5", "12.5", "12.5/13", "13", "13/13.5", "13.5", "13.5/14", "14"];

    dicHandicapMap = {  '*两/两球半':'-2.25',
                        '*两球':'-2.0',
                        '*球半/两':'-1.75',
                        '*球半':'-1.5',
                        '*一/球半':'-1.25',
                        '*一球':'-1.0',
                        '*半/一':'-0.75',
                        '*半球':'-0.5',
                        '*平/半':'-0.25',
                        '平手':'0.00',
                        '平/半':'0.25',
                        '半球':'0.5',
                        '半/一':'0.75',
                        '一球':'1.0',
                        '一/球半':'1.25',
                        '球半':'1.5',
                        '球半/两':'1.75',
                        '两球':'2.0',
                        '两/两球半':'2.25',
                        '两球半':'2.5'}
    if "澳门" in classIndexData.indexDataList[0].keys():
        dicData["fInitialHandicapX"] =  float(dicHandicapMap[classIndexData.indexDataList[0]["澳门"][0][8]])
        if dicData["fInitialHandicapX"] > 0:
            dicData["fInitialHandicapOver"] = float(classIndexData.indexDataList[0]["澳门"][0][7])
            dicData["fInitialHandicapUnder"] = float(classIndexData.indexDataList[0]["澳门"][0][9])
        else:
            dicData["fInitialHandicapOver"] = float(classIndexData.indexDataList[0]["澳门"][0][9])
            dicData["fInitialHandicapUnder"] = float(classIndexData.indexDataList[0]["澳门"][0][7])
        
        dicData["fInstantHandicapX"] = float(dicHandicapMap[classIndexData.indexDataList[0]["澳门"][1][8]])
        if dicData["fInstantHandicapX"] > 0:
            dicData["fInstantHandicapOver"] = float(classIndexData.indexDataList[0]["澳门"][1][7])
            dicData["fInstantHandicapUnder"] = float(classIndexData.indexDataList[0]["澳门"][1][9])
        else:
            dicData["fInstantHandicapOver"] = float(classIndexData.indexDataList[0]["澳门"][1][9])
            dicData["fInstantHandicapUnder"] = float(classIndexData.indexDataList[0]["澳门"][1][7])
        
    #stHandicapList  暂时不设置即时数据详细信息

    if "Crown" in classIndexData.indexDataList[1].keys():
        dicData["fInitialHandicapX_crown"] = float(dicHandicapMap[classIndexData.indexDataList[1]["Crown"][0][8]])
        if dicData["fInitialHandicapX_crown"] > 0:
            dicData["fInitialHandicapOver_crown"] = float(classIndexData.indexDataList[1]["Crown"][0][7])
            dicData["fInitialHandicapUnder_crown"] = float(classIndexData.indexDataList[1]["Crown"][0][9])
        else:
            dicData["fInitialHandicapOver_crown"] = float(classIndexData.indexDataList[1]["Crown"][0][9])
            dicData["fInitialHandicapUnder_crown"] = float(classIndexData.indexDataList[1]["Crown"][0][7])

        dicData["fInstantHandicapX_crown"] = float(dicHandicapMap[classIndexData.indexDataList[1]["Crown"][1][8]])
        if dicData["fInstantHandicapX_crown"] > 0:
            dicData["fInstantHandicapOver_crown"] = float(classIndexData.indexDataList[1]["Crown"][1][7])
            dicData["fInstantHandicapUnder_crown"] = float(classIndexData.indexDataList[1]["Crown"][1][9])
        else:
            dicData["fInstantHandicapOver_crown"] = float(classIndexData.indexDataList[1]["Crown"][1][9])
            dicData["fInstantHandicapUnder_crown"] = float(classIndexData.indexDataList[1]["Crown"][1][7])

    #print(dicData)
    return dicData
    #decodeGameData(dicData)


def decodeGameData(dicData):
    strJson = json.dumps(dicData)
    #print(strJson)
    strJson = strJson.replace("\"", "\\\"")
    
    if platform.system() == "Windows":
        exeName = "py_decode.exe"
    else:
        exeName = "py_decode"

    exePath = os.path.dirname(__file__) + "/c/" + exeName + " \"" + strJson + "\""
    r_v = os.system(exePath) 
    print(r_v)

if __name__ == "__main__":
    #test source data http://zq.win007.com/analysis/1743046sb.htm
     #初始化数据表格
    classH0V0Data = H0V0Data()
    praseDataH0V0(classH0V0Data, praseData(t2[2:-2]), praseData(t3[2:-2]))

    #初始化历史战绩
    classOldGameData = gameData(classH0V0Data)
    praseDataOld(classOldGameData, praseData(t1[2:]))

    classOldGameData.outputData()



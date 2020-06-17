# -*- coding: utf-8 -*- 

import sys
import json


class gameData:
    def __init__(self):
        self.iCount = 0             #列表数量
        self.iGameId = []            #id 用于查找数据
        self.sGameType = []         #类型
        self.sGameDate = []         #日期
        self.sGameHomeField = []    #主场
        self.sCore = []             #比分
        self.sCorner = []           #角球
        self.sAwayGroun = []        #客场
        self.fDataMain1 = {'皇冠':[], '澳门':[], 'Bet365':[], '易胜博':[], '12Bet':[]}   #主
        self.fDataTap = {'皇冠':[], '澳门':[], 'Bet365':[], '易胜博':[], '12Bet':[]}  #盘口
        self.fDataGuest1 = {'皇冠':[], '澳门':[], 'Bet365':[], '易胜博':[], '12Bet':[]}   #客
        self.fDataMain2 = {'皇冠':[], '澳门':[], 'Bet365':[], '易胜博':[], '12Bet':[]}   #主
        self.fDataAnd = {'皇冠':[], '澳门':[], 'Bet365':[], '易胜博':[], '12Bet':[]}   #和
        self.fDataGuest2 = {'皇冠':[], '澳门':[], 'Bet365':[], '易胜博':[], '12Bet':[]}   #客
        self.sPraseH0V0DIC = {}

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
    
        print(self.sPraseH0V0DIC)

    def findDatH0V0(self, liGameId, iTypeId, iPos):
        if liGameId in self.sPraseH0V0DIC.keys():
            for node in self.sPraseH0V0DIC[liGameId]:
                if iTypeId in node.keys():
                    return node[iTypeId][iPos]
            else:
                return ''
        else:
            return ''

    def setData(self, sPraseData):
        sNodeList = sPraseData.split(',')
        #i = 0
        #for node2 in sNodeList:
            #print(str(i) + " : " + node2)
        #    i += 1
        self.iGameId.append(sNodeList[15])
        self.sGameType.append(sNodeList[2])
        self.sGameDate.append(sNodeList[0])
        self.sGameHomeField.append(sNodeList[5].split('>')[1].split('<')[0])
        self.sCore.append(sNodeList[8] + '-' + sNodeList[9] + '(' + sNodeList[10] + ')')
        self.sCorner.append(sNodeList[16] + '-' + sNodeList[17])
        print(sNodeList[7])
        print(sNodeList)
        if sNodeList[7] != '':
            self.sAwayGroun.append(sNodeList[7].split('>')[1].split('<')[0])
        print("ddd " + sNodeList[15])
        self.fDataMain1["皇冠"].append(self.findDatH0V0(sNodeList[15], 0, 0))
        self.fDataMain1["澳门"].append(self.findDatH0V0(sNodeList[15], 80, 0))
        self.fDataMain1["Bet365"].append(self.findDatH0V0(sNodeList[15], 281, 0))
        #self.fDataMain1["易胜博"].append(self.findDatH0V0(sNodeList[15], 0, 0))
        self.fDataMain1["12Bet"].append(self.findDatH0V0(sNodeList[15], 18, 0))
        self.fDataTap["皇冠"].append(self.findDatH0V0(sNodeList[15], 0, 0))
        self.fDataTap["澳门"].append(self.findDatH0V0(sNodeList[15], 80, 0))
        self.fDataTap["Bet365"].append(self.findDatH0V0(sNodeList[15], 281, 0))
        #self.fDataTap["易胜博"].append(self.findDatH0V0(sNodeList[15], 0, 0))
        self.fDataTap["12Bet"].append(self.findDatH0V0(sNodeList[15], 18, 0))
        self.iCount += 1

 

f = open("/Users/hlc/workspace/SyncProject/python/py_request/test.txt", 'rb')
t1 = f.read()
f.close()

f = open("/Users/hlc/workspace/SyncProject/python/py_request/test2.txt", 'rb')
t2 = f.read()
f.close()

f = open("/Users/hlc/workspace/SyncProject/python/py_request/test3.txt", 'rb')
t3 = f.read()
f.close()

classOldGameData = gameData()
def praseData(sStr):
    sStrList = sStr.split('],[')
    #print(len(sStrList))
    for node in sStrList:
        #print("test : " + node)
        pass

    return sStrList

#解析历史战绩表格
def praseDataOld(sStrList):
    global classOldGameData
    for node in sStrList:
        print("test : " + node)
        classOldGameData.setData(node)

#解析对应数据表格
def praseDataH0V0(sStrListH0, sStrListV0):
    global classOldGameData
    classOldGameData.setDataH0V0(sStrListH0, sStrListV0)
    pass

if __name__ == "__main__":
    praseDataH0V0(praseData(t2[2:-2]), praseData(t3[2:-2]))
    praseDataOld(praseData(t1[2:]))





"""
#!/usr/bin/python
import json

data = [ { 'name' : '张三', 'age' : 25}, { 'name' : '李四', 'age' : 26} ]

jsonStr = json.dumps(data)
print(jsonStr)
"""

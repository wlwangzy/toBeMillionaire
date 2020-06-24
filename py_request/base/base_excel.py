
# -*- coding: utf-8 -*- 
import xlwt
import xlrd
from xlutils.copy import copy
import os
basedir = os.path.abspath(os.path.dirname(__file__))

def createExcel():
    book = xlwt.Workbook(encoding = "utf-8", style_compression = 0)
    sheet = book.add_sheet("数据归总", cell_overwrite_ok = True)
    sheet2 = book.add_sheet("数据来源", cell_overwrite_ok = True)

    return book, sheet, sheet2

def saveExcel(sFilePath, book):
    book.save(sFilePath)

def writeIntegralHeader(sheet, iStartLine, iStartColum):
    sheet.write(iStartLine, iStartColum, '赛')
    sheet.write(iStartLine, iStartColum + 1, '胜')
    sheet.write(iStartLine, iStartColum + 2, '平')
    sheet.write(iStartLine, iStartColum + 3, '负')
    sheet.write(iStartLine, iStartColum + 4, '得')
    sheet.write(iStartLine, iStartColum + 5, '失')
    sheet.write(iStartLine, iStartColum + 6, '净')
    sheet.write(iStartLine, iStartColum + 7, '得分')
    sheet.write(iStartLine, iStartColum + 8, '排名')
    sheet.write(iStartLine, iStartColum + 9, '胜率')

def writeIntegralBody(sheet, iStartLine, iStartColum, dataList):
    i = 0
    iLine = iStartLine
    for node in dataList:
        if i < 4:
            iCloum = iStartColum
        else:
            iCloum = iStartColum + 11

        if i == 4:
            iLine = iStartLine

        i += 1
        for dataKey in node:
            sheet.write(iLine, iCloum, dataKey)
            iCloum += 1
            for data in node[dataKey]:
                sheet.write(iLine, iCloum, data)
                iCloum += 1
        iLine += 1
    
    return iLine

def writeIntegralExcel(sheet, iStartLine, iStartColum, classIntegralData):
    #init table header
    sheet.write(iStartLine, iStartColum, classIntegralData.sLeftTableName)
    sheet.write(iStartLine, iStartColum + 11, classIntegralData.sRightTableName)
    iStartLine += 1
    sheet.write(iStartLine, iStartColum, "全场")
    writeIntegralHeader(sheet, iStartLine , iStartColum + 1)
    sheet.write(iStartLine, iStartColum + 11, "全场")
    writeIntegralHeader(sheet, iStartLine , iStartColum + 12)
    iStartLine += 1
    iStartLine = writeIntegralBody(sheet, iStartLine, iStartColum, classIntegralData.integralDataList["全场"])
    
    sheet.write(iStartLine, iStartColum, "半场")
    writeIntegralHeader(sheet, iStartLine , iStartColum + 1)
    sheet.write(iStartLine, iStartColum + 11, "半场")
    writeIntegralHeader(sheet, iStartLine , iStartColum + 12)
    iStartLine += 1
    iStartLine = writeIntegralBody(sheet, iStartLine, iStartColum, classIntegralData.integralDataList["半场"])

    return iStartLine
    
def writeIndexHeader(sheet, iStartLine, iStartColum):
    #LINE 0
    sheet.write(iStartLine, iStartColum, '欧洲指数')
    sheet.write(iStartLine, iStartColum + 3, '欧转亚盘')
    sheet.write(iStartLine, iStartColum + 6, '实际最新亚盘')
    sheet.write(iStartLine, iStartColum + 9, '大小球')

    #LINE 1
    iStartLine += 1
    sheet.write(iStartLine, iStartColum, '主胜')
    sheet.write(iStartLine, iStartColum + 1, '和局')
    sheet.write(iStartLine, iStartColum + 2, '客胜')
    sheet.write(iStartLine, iStartColum + 3, '主队')
    sheet.write(iStartLine, iStartColum + 4, '让球')
    sheet.write(iStartLine, iStartColum + 5, '客队')
    sheet.write(iStartLine, iStartColum + 6, '主队')
    sheet.write(iStartLine, iStartColum + 7, '让球')
    sheet.write(iStartLine, iStartColum + 8, '客队')
    sheet.write(iStartLine, iStartColum + 9, '大球')
    sheet.write(iStartLine, iStartColum + 10, '盘口')
    sheet.write(iStartLine, iStartColum + 11, '小球')

def writeIndexBody(sheet, iStartLine, iStartColum, classIndexDataNode):
    for dataKey in classIndexDataNode:
        sheet.write(iStartLine, iStartColum, dataKey)
        sheet.write(iStartLine, iStartColum + 1, '初盘')
        sheet.write(iStartLine + 1, iStartColum + 1, '终盘')
        sheet.write(iStartLine + 2, iStartColum + 1, '滚球')
        i = 0
        iStartColum += 2
        while i < 14:
            if i == 6 or i == 10:
                i += 1
            sheet.write(iStartLine, iStartColum, classIndexDataNode[dataKey][0][i])
            sheet.write(iStartLine + 1, iStartColum, classIndexDataNode[dataKey][1][i])
            sheet.write(iStartLine + 2, iStartColum, classIndexDataNode[dataKey][2][i])
            iStartColum += 1
            i += 1

    iStartLine += 3

    return iStartLine


def writeIndexExcel(sheet, iStartLine, iStartColum, classIndexData):
    #classIndexData.outputData()
    writeIndexHeader(sheet, iStartLine, iStartColum + 2)
    iStartLine += 2
    for node in classIndexData.indexDataList:
        iStartLine = writeIndexBody(sheet, iStartLine, iStartColum, node)

    return iStartLine

def writeHistoryGameHeader(sheet, iStartLine, iStartColum):
    #LINE 0
    sheet.write(iStartLine, iStartColum, '对赛往绩')

    #LINE 1
    iStartLine += 1
    sheet.write(iStartLine, iStartColum, '类型')
    iStartColum += 1
    sheet.write(iStartLine, iStartColum, '日期')
    iStartColum += 1
    sheet.write(iStartLine, iStartColum, '主场')
    iStartColum += 1
    sheet.write(iStartLine, iStartColum, '比分(半场)')
    iStartColum += 1
    sheet.write(iStartLine, iStartColum, '角球')
    iStartColum += 1
    sheet.write(iStartLine, iStartColum, '客场')
    iStartColum += 2
    sheet.write(iStartLine, iStartColum, '主')
    iStartColum += 1
    sheet.write(iStartLine, iStartColum, '盘口')
    iStartColum += 1
    sheet.write(iStartLine, iStartColum, '客')
    iStartColum += 2
    sheet.write(iStartLine, iStartColum, '主')
    iStartColum += 1
    sheet.write(iStartLine, iStartColum, '和')
    iStartColum += 1
    sheet.write(iStartLine, iStartColum, '客')
    iStartColum += 1
    sheet.write(iStartLine, iStartColum, '胜负')
    iStartColum += 1
    #sheet.write(iStartLine, iStartColum, '让球')
    #iStartColum += 1
    #sheet.write(iStartLine, iStartColum, '大小')
    #iStartColum += 1

def writeGameBodyDataNode(sheet, iStartLine, iStartColum, mapData, sPos):
    #data
    sheet.write(iStartLine, iStartColum, sPos + ' 初盘')
    sheet.write(iStartLine + 1, iStartColum, sPos + ' 终盘')
    iStartColum += 1
    sheet.write(iStartLine, iStartColum, mapData[sPos]['start'][0])
    sheet.write(iStartLine + 1, iStartColum, mapData[sPos]['end'][0])
    sheet.write(iStartLine, iStartColum + 1, mapData[sPos]['start'][1])
    sheet.write(iStartLine + 1, iStartColum + 1, mapData[sPos]['end'][1])
    sheet.write(iStartLine, iStartColum + 2, mapData[sPos]['start'][2])
    sheet.write(iStartLine + 1, iStartColum + 2, mapData[sPos]['end'][2])


def writeGameBody(sheet, iStartLine, iStartColum, classGameData, i):
    sheet.write(iStartLine, iStartColum, classGameData.sGameType[i])
    iStartColum += 1
    sheet.write(iStartLine, iStartColum, classGameData.sGameDate[i])
    iStartColum += 1
    sheet.write(iStartLine, iStartColum, classGameData.sGameHomeField[i])
    iStartColum += 1
    sheet.write(iStartLine, iStartColum, classGameData.sCore[i])
    iStartColum += 1
    sheet.write(iStartLine, iStartColum, classGameData.sCorner[i])
    iStartColum += 1
    sheet.write(iStartLine, iStartColum, classGameData.sAwayGroun[i])
    iStartColum += 1
    sheet.write(iStartLine, iStartColum + 8, classGameData.sGameResult[i])
    #data
    writeGameBodyDataNode(sheet, iStartLine, iStartColum, classGameData.fDataMap1[i], '澳门')
    writeGameBodyDataNode(sheet, iStartLine, iStartColum + 4, classGameData.fDataMap2[i], '澳门')
    iStartLine += 2
    writeGameBodyDataNode(sheet, iStartLine, iStartColum, classGameData.fDataMap1[i], '皇冠')
    writeGameBodyDataNode(sheet, iStartLine, iStartColum + 4, classGameData.fDataMap2[i], '皇冠')
    iStartLine += 2


    
    return iStartLine

def writeHistoryGameData(sheet, iStartLine, iStartColum, classHistroyGameData):
    #classHistroyGameData.outputData()
    writeHistoryGameHeader(sheet, iStartLine, iStartColum)
    iStartLine += 2
    i = 0
    while i < classHistroyGameData.iCount:
        iStartLine = writeGameBody(sheet, iStartLine, iStartColum, classHistroyGameData, i)
        i += 1
    return iStartLine

def writeInGameData1Header(sheet, iStartLine, iStartColum):
    #LINE 0
    sheet.write(iStartLine, iStartColum, '近期战绩')

    #LINE 1
    iStartLine += 1
    sheet.write(iStartLine, iStartColum, '类型')
    iStartColum += 1
    sheet.write(iStartLine, iStartColum, '日期')
    iStartColum += 1
    sheet.write(iStartLine, iStartColum, '主场')
    iStartColum += 1
    sheet.write(iStartLine, iStartColum, '比分(半场)')
    iStartColum += 1
    sheet.write(iStartLine, iStartColum, '角球')
    iStartColum += 1
    sheet.write(iStartLine, iStartColum, '客场')
    iStartColum += 2
    sheet.write(iStartLine, iStartColum, '主')
    iStartColum += 1
    sheet.write(iStartLine, iStartColum, '盘口')
    iStartColum += 1
    sheet.write(iStartLine, iStartColum, '客')
    iStartColum += 2
    sheet.write(iStartLine, iStartColum, '主')
    iStartColum += 1
    sheet.write(iStartLine, iStartColum, '和')
    iStartColum += 1
    sheet.write(iStartLine, iStartColum, '客')
    iStartColum += 1
    sheet.write(iStartLine, iStartColum, '胜负')
    iStartColum += 1
    #sheet.write(iStartLine, iStartColum, '让球')
    #iStartColum += 1
    #sheet.write(iStartLine, iStartColum, '大小')
    #iStartColum += 1

def writeInGameData1(sheet, iStartLine, iStartColum, classInGameData1):
    #classHistroyGameData.outputData()
    writeInGameData1Header(sheet, iStartLine, iStartColum)
    iStartLine += 2
    i = 0
    while i < classInGameData1.iCount:
        iStartLine = writeGameBody(sheet, iStartLine, iStartColum, classInGameData1, i)
        i += 1
    return iStartLine

def writeInGameData2(sheet, iStartLine, iStartColum, classInGameData2):
    #classHistroyGameData.outputData()
    writeInGameData1Header(sheet, iStartLine, iStartColum)
    iStartLine += 2
    i = 0
    while i < classInGameData2.iCount:
        iStartLine = writeGameBody(sheet, iStartLine, iStartColum, classInGameData2, i)
        i += 1
    return iStartLine


def writeAllGameHeader(sheet, iStartLine, iStartColum):
    #LINE 0
    sheet.write(iStartLine, iStartColum, '总结表格')

    #LINE 1
    iStartLine += 1
    sheet.write(iStartLine, iStartColum, '日期')
    iStartColum += 1
    sheet.write(iStartLine, iStartColum, '类型')
    iStartColum += 1
    sheet.write(iStartLine, iStartColum, '主场')
    iStartColum += 1
    sheet.write(iStartLine, iStartColum, '客场')
    iStartColum += 1
    sheet.write(iStartLine, iStartColum, '比分(半场)')
    iStartColum += 1
    sheet.write(iStartLine, iStartColum, '胜负')
    iStartColum += 1
    #write qdas
    sheet.write(iStartLine, iStartColum, "qdsa")
    iStartColum += 1
    sheet.write(iStartLine, iStartColum, '初盘/终盘')
    iStartColum += 1
    sheet.write(iStartLine, iStartColum, '总盘口')
    iStartColum += 1
    sheet.write(iStartLine, iStartColum, '主')
    iStartColum += 1
    sheet.write(iStartLine, iStartColum, '盘口')
    iStartColum += 1
    sheet.write(iStartLine, iStartColum, '客')
    iStartColum += 1
    #sheet.write(iStartLine, iStartColum, '让球')
    #iStartColum += 1
    #sheet.write(iStartLine, iStartColum, '大小')
    #iStartColum += 1

def writeAllGameBodyDataNode(sheet, iStartLine, iStartColum, mapData, sPos):
    #data
    sheet.write(iStartLine, iStartColum, sPos + ' 初盘')
    sheet.write(iStartLine + 1, iStartColum, sPos + ' 终盘')
    iStartColum += 1
    sheet.write(iStartLine, iStartColum, mapData[sPos]['start'][1])
    sheet.write(iStartLine + 1, iStartColum, mapData[sPos]['end'][1])
    iStartColum += 1
    sheet.write(iStartLine, iStartColum, mapData[sPos]['start'][0])
    sheet.write(iStartLine + 1, iStartColum, mapData[sPos]['end'][0])
    sheet.write(iStartLine, iStartColum + 1, mapData[sPos]['start'][1])
    sheet.write(iStartLine + 1, iStartColum + 1, mapData[sPos]['end'][1])
    sheet.write(iStartLine, iStartColum + 2, mapData[sPos]['start'][2])
    sheet.write(iStartLine + 1, iStartColum + 2, mapData[sPos]['end'][2])

    gameDataDic1 = addWebGameDicNode(sPos + ' 初盘', mapData[sPos]['start'][1], mapData[sPos]['start'][0], mapData[sPos]['start'][2])
    gameDataDic2 = addWebGameDicNode(sPos + ' 终盘', mapData[sPos]['end'][1], mapData[sPos]['end'][0], mapData[sPos]['end'][2])

    return gameDataDic1, gameDataDic2

def createWebDic(sGameDate, sGameType, sGameHomeField, sAwayGroun, sCore, sGameResult):
    gameDataDic = {}
    gameDataDic["sGameDate"] = sGameDate
    gameDataDic["sGameType"] = sGameType
    gameDataDic["sGameHomeField"] = sGameHomeField
    gameDataDic["sAwayGroun"] = sAwayGroun
    gameDataDic["sCore"] = sCore
    gameDataDic["sGameResult"] = sGameResult
    gameDataDic["qdsa"] = ""

    return gameDataDic

def addWebGameDicNode(sDataName, sPanData, sZhu, sKeData):
    #gameDataDicNode = gameDataDic
    gameDataDicNode = {}
    gameDataDicNode["sDataName"] = sDataName
    gameDataDicNode["sPanAll"] = sPanData
    gameDataDicNode["sZhuData"] = sZhu
    gameDataDicNode["sPan"] = sPanData
    gameDataDicNode["sKeData"] = sKeData

    return gameDataDicNode


def writeAllGameBody(sheet, iStartLine, iStartColum, classGameData, i, gameDataList):
    sheet.write(iStartLine, iStartColum, classGameData.sGameDate[i])
    iStartColum += 1
    sheet.write(iStartLine, iStartColum, classGameData.sGameType[i])
    iStartColum += 1
    sheet.write(iStartLine, iStartColum, classGameData.sGameHomeField[i])
    iStartColum += 1
    sheet.write(iStartLine, iStartColum, classGameData.sAwayGroun[i])
    iStartColum += 1
    sheet.write(iStartLine, iStartColum, classGameData.sCore[i])
    iStartColum += 1
    sheet.write(iStartLine, iStartColum, classGameData.sGameResult[i])
    #write qdas
    iStartColum += 1
    
    iStartColum += 1

    gameDataDic = createWebDic(classGameData.sGameDate[i], classGameData.sGameType[i], classGameData.sGameHomeField[i],
                                            classGameData.sAwayGroun[i], classGameData.sCore[i], classGameData.sGameResult[i])
    gameDataDicNone = createWebDic("", "", "", "", "", "")
    #data
    gameDataDic1, gameDataDic2 = writeAllGameBodyDataNode(sheet, iStartLine, iStartColum, classGameData.fDataMap1[i], '澳门')
    gameDataDic1 = dict(gameDataDic1, **gameDataDic)
    gameDataDic2 = dict(gameDataDic2, **gameDataDicNone)
    gameDataList.append(gameDataDic1)
    gameDataList.append(gameDataDic2)
    iStartLine += 2
    gameDataDic1, gameDataDic2  = writeAllGameBodyDataNode(sheet, iStartLine, iStartColum, classGameData.fDataMap1[i], '皇冠')
    gameDataDic1 = dict(gameDataDic1, **gameDataDicNone)
    gameDataDic2 = dict(gameDataDic2, **gameDataDicNone)
    gameDataList.append(gameDataDic1)
    gameDataList.append(gameDataDic2)
    iStartLine += 2

    
    return iStartLine, gameDataList

def writeAllGameData(sheet, iStartLine, iStartColum, classHistroyGameData):
    #classHistroyGameData.outputData()
    writeAllGameHeader(sheet, iStartLine, iStartColum)
    iStartLine += 2
    i = 0
    gameDataList = []
    while i < classHistroyGameData.iCount:
        iStartLine, gameDataList = writeAllGameBody(sheet, iStartLine, iStartColum, classHistroyGameData, i, gameDataList)
        i += 1
    return iStartLine, gameDataList

def updateExcelData(outPathFile, jsonDic):
    rBook = xlrd.open_workbook(outPathFile)
    wBook = copy(rBook)
    wSheet = wBook.get_sheet(0)
    iStartLine = 2
    iStartColum = 6
    for node in jsonDic:
        #print node
        #print node["qdsa"]
        wSheet.write(iStartLine, iStartColum, node["qdsa"])
        iStartLine += 1

    wBook.save(outPathFile)

def writeExcelData(outPathFile, classHistroyGameData = None, classInGameData1 = None, classInGameData2 = None, classIndexData = None, classIntegralData = None):
    book, sheet, sheet2 = createExcel()
    iStartLine = 0
    iStartColum = 0

    #写入联赛积分排名数据
    iStartLine = writeIntegralExcel(sheet2, iStartLine, iStartColum, classIntegralData)
    iStartLine = writeIndexExcel(sheet2, iStartLine + 10, iStartColum, classIndexData)
    iStartLine = writeHistoryGameData(sheet2, iStartLine + 10, iStartColum, classHistroyGameData)
    iStartLine = writeInGameData1(sheet2, iStartLine + 10, iStartColum, classInGameData1)
    iStartLine = writeInGameData2(sheet2, iStartLine + 10, iStartColum, classInGameData2)

    #写入总结数据
    iStartLine = 0
    iStartLine, gameDataList = writeAllGameData(sheet, iStartLine, iStartColum, classHistroyGameData)
    #for node in gameDataList:
    #    print node

    book.save(outPathFile)

    return  gameDataList

if __name__ == "__main__":
    book, sheet = createExcel()

    sheet.write(0, 0, "EnglishName") #其中，"0, 0"指定表中的单元格，"EnglishName"是向该单元格中写入的内容
    sheet.write(1, 0, "MaYi")
    sheet.write(0, 1, "中文名字")
    sheet.write(1, 1, "蚂蚁")
    #最后，将以上操作保存到指定的Excel文件中
    book.save(basedir + "/../name.xls")

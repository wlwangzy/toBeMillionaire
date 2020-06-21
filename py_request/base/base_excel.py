
# -*- coding: utf-8 -*- 
import xlwt
import os
basedir = os.path.abspath(os.path.dirname(__file__))

def createExcel():
    book = xlwt.Workbook(encoding = "utf-8", style_compression = 0)
    sheet = book.add_sheet("sheet1", cell_overwrite_ok = True)
    
    return book, sheet

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


def writeExcelData(classHistroyGameData = None, classInGameData1 = None, classInGameData2 = None, classIndexData = None, classIntegralData = None):
    book, sheet = createExcel()
    iStartLine = 0
    iStartColum = 0

    #写入联赛积分排名数据
    iStartLine = writeIntegralExcel(sheet, iStartLine, iStartColum, classIntegralData)
    iStartLine = writeIndexExcel(sheet, iStartLine + 10, iStartColum, classIndexData)
    iStartLine = writeHistoryGameData(sheet, iStartLine + 10, iStartColum, classHistroyGameData)
    iStartLine = writeInGameData1(sheet, iStartLine + 10, iStartColum, classInGameData1)
    iStartLine = writeInGameData2(sheet, iStartLine + 10, iStartColum, classInGameData2)

    book.save(basedir + "/../test.xls")


if __name__ == "__main__":
    book, sheet = createExcel()

    sheet.write(0, 0, "EnglishName") #其中，"0, 0"指定表中的单元格，"EnglishName"是向该单元格中写入的内容
    sheet.write(1, 0, "MaYi")
    sheet.write(0, 1, "中文名字")
    sheet.write(1, 1, "蚂蚁")
    #最后，将以上操作保存到指定的Excel文件中
    book.save(basedir + "/../name.xls")

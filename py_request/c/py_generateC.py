import os

INCFILE = os.path.dirname(__file__) + '/py_decode.h'
SRCFILE = os.path.dirname(__file__) + '/py_decode.c'

def checkType(sType):
    if "[" in sType:
        return sType.split("[")[0]
    else:
        return sType
        
def checkStrNode(strNode):
    strAppend = "    "
    sType = "" 
    if "i" == strNode[0] or "b" == strNode[0]:
        strAppend += "DECJSONITEM_INT"
        sType = "%d"
        initData = 0
    elif "f" == strNode[0]:
        strAppend += "DECJSONITEM_FLOAT"
        sType = "%f"
        initData = 0.0
    elif "c" == strNode[0]:
        strAppend += "DECJSONITEM_STR"
        sType = "%s"
        initData = "c"
    else:
        strAppend = ""
        sType = ""
        initData = ""

    return strAppend, sType, initData

def initWriteData(listNode):
    listWriteDecData = []
    listWriteOutData = []
    listWriteInitData = []
    
    for strNode in listNode:
        strNode = checkType(strNode)
        strAppend, sType, initData = checkStrNode(strNode)
        if strAppend is "":
            pass #do check list or otther
        strAppend += "(pstDecodeData, pJsonData, " + strNode +  ")\n"
        listWriteDecData.append(strAppend)
        strAppend = "    logI(\"" + strNode + " " + sType + " \\n\", pstDecodeData->" + strNode + ");\n"
        listWriteOutData.append(strAppend)
        if initData is not "c":
            strAppend = "   pstDecodeData->" + strNode + " = " + str(initData) + ";\n"
        else:
            strAppend = "   memset(pstDecodeData->" + strNode + ", 0, sizeof(pstDecodeData->" + strNode + "));\n"
        listWriteInitData.append(strAppend)

    return listWriteDecData, listWriteOutData, listWriteInitData

def findIncChild(strFather, strFindNode):
    with open(INCFILE, 'r') as f:
        strList = f.readlines()
        


def findIncName():
    with open(INCFILE, 'r') as f:
        strList = f.readlines()
        #print(strList)
        iStrucFlag = 0;
        listNode = []
        for strNode in strList:
            #print(strNode)
            if "DEFAnalysParam" in strNode:
                iStrucFlag = 1
            if "}" in strNode and iStrucFlag is 1:
                iStrucFlag = 0
            if iStrucFlag is 1 and ("Z" in strNode):
                #print(strNode)
                listNode.append(strNode.split(';')[0].split(' ')[-1])
            if "PST" in strNode:
                tmpList = findIncChild(tmpList, strNode.split(';')[0].split(' ')[-1], strNode.split(';')[0].split(None,str.split(" "))[-2])
                listNode.append(tmpList)
    return listNode

def writeSrcFile(strFind, listWriteDecData):
    iStart = 0
    iEnd = 0
    iPos = 0
    with open(SRCFILE, 'r') as f:
        strList = f.readlines()
        for strNode in strList:
            if strFind in strNode:
                iStart = iPos
            if iStart is not 0 and "}" in strNode:
                iEnd = iPos
                break
            iPos += 1
    
    with open(SRCFILE, 'w') as f:
        writeData = strList[:iStart+2] + listWriteDecData + strList[iEnd:]
        print(writeData)
        f.writelines(writeData)

    
        
    print("Ok")

if __name__ == "__main__":
    print(INCFILE)
    listWriteDecData, listWriteOutData, listWriteInitData = initWriteData(findIncName())
    writeSrcFile("void pyDec_getJsonStr(AnalysParam *pstDecodeData, cJSON *pJsonData)", listWriteDecData)
    writeSrcFile("void pyDec_OutPutData(AnalysParam *pstDecodeData)", listWriteOutData)
    writeSrcFile("void pyDec_InitData(AnalysParam *pstDecodeData)", listWriteInitData)
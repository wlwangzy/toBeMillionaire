
def checkStrNode(strNode):
    strAppend = "    "
    if "i" == strNode[0]:
        strAppend += "DECJSONITEM_INT"
    elif "f" == strNode[0]:
        strAppend += "DECJSONITEM_FLOAT"
    elif "c" == strNode[0]:
        strAppend += "DECJSONITEM_STR"
    else:
        strAppend = ""

    return strAppend

def initWriteData(listNode):
    listWriteData = []
    
    for strNode in listNode:
        strAppend = checkStrNode(strNode)
        if strAppend is "":
            pass #do check list or otther
        strAppend += "(pstDecodeData, pJsonData, " + strNode +  ")\r\n"
        listWriteData.append(strAppend)

    return listWriteData

def findIncName():
    with open('py_decode.h', 'r') as f:
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
            if iStrucFlag is 1 and ("Z" in strNode):#or "PST" in strNode):
                #print(strNode)
                listNode.append(strNode.split(';')[0].split(' ')[-1])

    return listNode

def writeSrcFile(listWriteData):
    iStart = 0
    iEnd = 0
    iPos = 0
    with open('py_decode.c', 'r') as f:
        strList = f.readlines()
        for strNode in strList:
            if "void pyDec_getJsonStr(AnalysParam *pstDecodeData, cJSON *pJsonData)" in strNode:
                iStart = iPos
            if iStart is not 0 and "}" in strNode:
                iEnd = iPos
                break
            iPos += 1
    
    with open('py_decode.c', 'w') as f:
        writeData = strList[:iStart+2] + listWriteData + strList[iEnd:]
        print(writeData)
        f.writelines(writeData)
        
    return "Ok"
if __name__ == "__main__":
    print(writeSrcFile(initWriteData(findIncName())))
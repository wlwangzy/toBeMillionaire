#include <stdio.h>
#include "cJSON.c"
#include "cJSON.h"
#include "py_decode.h"


#define DECJSONITEM_INT(pstDecodeData, json, str)do{ \
									cJSON *item = cJSON_GetObjectItem(json, #str); \
									if(item) \
										pstDecodeData->str = item->valueint; \
									else \
										logW("decode error "#str "\n");\
								}while(0); 

#define DECJSONITEM_FLOAT(pstDecodeData, json, str)do{ \
									cJSON *item = cJSON_GetObjectItem(json, #str); \
									if(item)\
										pstDecodeData->str = item->valuedouble; \
									else \
										logW("decode error "#str "\n");\
								}while(0);

#define DECJSONITEM_STR(pstDecodeData, json, str)do{ \
									cJSON *item = cJSON_GetObjectItem(json, #str); \
									if(item)\
										memcpy(pstDecodeData->str, item->valuestring, sizeof(pstDecodeData->str)); \
									else \
										logW("decode error "#str "\n");\
								}while(0); 


void pyDec_getJsonStr(AnalysParam *pstDecodeData, cJSON *pJsonData)
{
    DECJSONITEM_INT(pstDecodeData, pJsonData, bNeutral)
    DECJSONITEM_STR(pstDecodeData, pJsonData, cType)
    DECJSONITEM_INT(pstDecodeData, pJsonData, iHomeRank)
    DECJSONITEM_INT(pstDecodeData, pJsonData, iHomeRecentWin)
    DECJSONITEM_INT(pstDecodeData, pJsonData, iHomeRecentDraws)
    DECJSONITEM_INT(pstDecodeData, pJsonData, iHomeRecentLose)
    DECJSONITEM_INT(pstDecodeData, pJsonData, iHomeRecentHomeWin)
    DECJSONITEM_INT(pstDecodeData, pJsonData, iHomeRecentHomeDraws)
    DECJSONITEM_INT(pstDecodeData, pJsonData, iHomeRecentHomeLose)
    DECJSONITEM_INT(pstDecodeData, pJsonData, iAwayRank)
    DECJSONITEM_INT(pstDecodeData, pJsonData, iAwayRecentWin)
    DECJSONITEM_INT(pstDecodeData, pJsonData, iAwayRecentDraws)
    DECJSONITEM_INT(pstDecodeData, pJsonData, iAwayRecentLose)
    DECJSONITEM_INT(pstDecodeData, pJsonData, iAwayRecentAwayWin)
    DECJSONITEM_INT(pstDecodeData, pJsonData, iAwayRecentAwayDraws)
    DECJSONITEM_INT(pstDecodeData, pJsonData, iAwayRecentAwayLose)
    DECJSONITEM_INT(pstDecodeData, pJsonData, iVsRecHomeWin)
    DECJSONITEM_INT(pstDecodeData, pJsonData, iVsRecHomeDraws)
    DECJSONITEM_INT(pstDecodeData, pJsonData, iVsRecHomeLose)
    DECJSONITEM_INT(pstDecodeData, pJsonData, iQdsa)
    DECJSONITEM_FLOAT(pstDecodeData, pJsonData, fInitialHandicapX)
    DECJSONITEM_FLOAT(pstDecodeData, pJsonData, fInitialHandicapOver)
    DECJSONITEM_FLOAT(pstDecodeData, pJsonData, fInitialHandicapUnder)
    DECJSONITEM_FLOAT(pstDecodeData, pJsonData, fInstantHandicapX)
    DECJSONITEM_FLOAT(pstDecodeData, pJsonData, fInstantHandicapOver)
    DECJSONITEM_FLOAT(pstDecodeData, pJsonData, fInstantHandicapUnder)
    DECJSONITEM_FLOAT(pstDecodeData, pJsonData, fInitialHandicapX_crown)
    DECJSONITEM_FLOAT(pstDecodeData, pJsonData, fInitialHandicapOver_crown)
    DECJSONITEM_FLOAT(pstDecodeData, pJsonData, fInitialHandicapUnder_crown)
    DECJSONITEM_FLOAT(pstDecodeData, pJsonData, fInstantHandicapX_crown)
    DECJSONITEM_FLOAT(pstDecodeData, pJsonData, fInstantHandicapOver_crown)
    DECJSONITEM_FLOAT(pstDecodeData, pJsonData, fInstantHandicapUnder_crown)
}

void pyDec_InitData(AnalysParam *pstDecodeData)
{
   pstDecodeData->bNeutral = 0;
   memset(pstDecodeData->cType, 0, sizeof(pstDecodeData->cType));
   pstDecodeData->iHomeRank = 0;
   pstDecodeData->iHomeRecentWin = 0;
   pstDecodeData->iHomeRecentDraws = 0;
   pstDecodeData->iHomeRecentLose = 0;
   pstDecodeData->iHomeRecentHomeWin = 0;
   pstDecodeData->iHomeRecentHomeDraws = 0;
   pstDecodeData->iHomeRecentHomeLose = 0;
   pstDecodeData->iAwayRank = 0;
   pstDecodeData->iAwayRecentWin = 0;
   pstDecodeData->iAwayRecentDraws = 0;
   pstDecodeData->iAwayRecentLose = 0;
   pstDecodeData->iAwayRecentAwayWin = 0;
   pstDecodeData->iAwayRecentAwayDraws = 0;
   pstDecodeData->iAwayRecentAwayLose = 0;
   pstDecodeData->iVsRecHomeWin = 0;
   pstDecodeData->iVsRecHomeDraws = 0;
   pstDecodeData->iVsRecHomeLose = 0;
   pstDecodeData->iQdsa = 0;
   pstDecodeData->fInitialHandicapX = 0.0;
   pstDecodeData->fInitialHandicapOver = 0.0;
   pstDecodeData->fInitialHandicapUnder = 0.0;
   pstDecodeData->fInstantHandicapX = 0.0;
   pstDecodeData->fInstantHandicapOver = 0.0;
   pstDecodeData->fInstantHandicapUnder = 0.0;
   pstDecodeData->fInitialHandicapX_crown = 0.0;
   pstDecodeData->fInitialHandicapOver_crown = 0.0;
   pstDecodeData->fInitialHandicapUnder_crown = 0.0;
   pstDecodeData->fInstantHandicapX_crown = 0.0;
   pstDecodeData->fInstantHandicapOver_crown = 0.0;
   pstDecodeData->fInstantHandicapUnder_crown = 0.0;
}

void pyDec_OutPutData(AnalysParam *pstDecodeData)
{
    logI("bNeutral %d \n", pstDecodeData->bNeutral);
    logI("cType %s \n", pstDecodeData->cType);
    logI("iHomeRank %d \n", pstDecodeData->iHomeRank);
    logI("iHomeRecentWin %d \n", pstDecodeData->iHomeRecentWin);
    logI("iHomeRecentDraws %d \n", pstDecodeData->iHomeRecentDraws);
    logI("iHomeRecentLose %d \n", pstDecodeData->iHomeRecentLose);
    logI("iHomeRecentHomeWin %d \n", pstDecodeData->iHomeRecentHomeWin);
    logI("iHomeRecentHomeDraws %d \n", pstDecodeData->iHomeRecentHomeDraws);
    logI("iHomeRecentHomeLose %d \n", pstDecodeData->iHomeRecentHomeLose);
    logI("iAwayRank %d \n", pstDecodeData->iAwayRank);
    logI("iAwayRecentWin %d \n", pstDecodeData->iAwayRecentWin);
    logI("iAwayRecentDraws %d \n", pstDecodeData->iAwayRecentDraws);
    logI("iAwayRecentLose %d \n", pstDecodeData->iAwayRecentLose);
    logI("iAwayRecentAwayWin %d \n", pstDecodeData->iAwayRecentAwayWin);
    logI("iAwayRecentAwayDraws %d \n", pstDecodeData->iAwayRecentAwayDraws);
    logI("iAwayRecentAwayLose %d \n", pstDecodeData->iAwayRecentAwayLose);
    logI("iVsRecHomeWin %d \n", pstDecodeData->iVsRecHomeWin);
    logI("iVsRecHomeDraws %d \n", pstDecodeData->iVsRecHomeDraws);
    logI("iVsRecHomeLose %d \n", pstDecodeData->iVsRecHomeLose);
    logI("iQdsa %d \n", pstDecodeData->iQdsa);
    logI("fInitialHandicapX %f \n", pstDecodeData->fInitialHandicapX);
    logI("fInitialHandicapOver %f \n", pstDecodeData->fInitialHandicapOver);
    logI("fInitialHandicapUnder %f \n", pstDecodeData->fInitialHandicapUnder);
    logI("fInstantHandicapX %f \n", pstDecodeData->fInstantHandicapX);
    logI("fInstantHandicapOver %f \n", pstDecodeData->fInstantHandicapOver);
    logI("fInstantHandicapUnder %f \n", pstDecodeData->fInstantHandicapUnder);
    logI("fInitialHandicapX_crown %f \n", pstDecodeData->fInitialHandicapX_crown);
    logI("fInitialHandicapOver_crown %f \n", pstDecodeData->fInitialHandicapOver_crown);
    logI("fInitialHandicapUnder_crown %f \n", pstDecodeData->fInitialHandicapUnder_crown);
    logI("fInstantHandicapX_crown %f \n", pstDecodeData->fInstantHandicapX_crown);
    logI("fInstantHandicapOver_crown %f \n", pstDecodeData->fInstantHandicapOver_crown);
    logI("fInstantHandicapUnder_crown %f \n", pstDecodeData->fInstantHandicapUnder_crown);
}

int main(int argc, const char *argv[])
{
	AnalysParam stDecodeData;
	//const char test[] = "{\"iHomeRank\" : 1}";
	cJSON *pJsonData = NULL;
	
	pJsonData = cJSON_Parse(argv[1]);
	//pJsonData = cJSON_Parse(test); //TEST CODE
    if(!pJsonData)
    {
        logE("json is failed \n");
        return 0;
    }
    
    pyDec_InitData(&stDecodeData);
	pyDec_getJsonStr(&stDecodeData, pJsonData);
	pyDec_OutPutData(&stDecodeData);
	logI("decode data is ok\n");

    return 0;
	//get stDecodeData do decode data
}
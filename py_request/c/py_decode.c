#include <stdio.h>
#include "cJSON.c"
#include "cJSON.h"
#include "py_decode.h"


#define DECJSONITEM_INT(pstDecodeData, json, str)do{ \
									cJSON *item = cJSON_GetObjectItem(json, #str); \
									if(item) \
										pstDecodeData->str = item->valueint; \
									else \
										logW("decode error \n");\
								}while(0); 

#define DECJSONITEM_FLOAT(pstDecodeData, json, str)do{ \
									cJSON *item = cJSON_GetObjectItem(json, #str); \
									if(item)\
										pstDecodeData->str = item->valuedouble; \
									else \
										logW("decode error \n"); \										
								}while(0); 

#define DECJSONITEM_STR(pstDecodeData, json, str)do{ \
									cJSON *item = cJSON_GetObjectItem(json, #str); \
									if(item)\
										pstDecodeData->str = item->valuestring; \
									else \
										logW("decode error \n");\
								}while(0); 

void pyDec_getJsonStr(AnalysParam *pstDecodeData, cJSON *pJsonData)
{
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

void pyDec_OutPutData(AnalysParam *pstDecodeData)
{
	logI("iHomeRank %d", pstDecodeData->iHomeRank);
}

int main(int argc, const char *argv[])
{
	AnalysParam stDecodeData;
	const char test[] = "{\"iHomeRank\" : 1}";
	cJSON *pJsonData = NULL;
	
	pJsonData = cJSON_Parse(argv[1]);
	pJsonData = cJSON_Parse(test);
	pyDec_getJsonStr(&stDecodeData, pJsonData);
	
	printf("ok %d \n", stDecodeData.iHomeRank);
	//get stDecodeData do decode data
}
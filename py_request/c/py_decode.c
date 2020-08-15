#include <stdio.h>
#include "cJSON.c"
#include "cJSON.h"
#include "py_decode.h"


#define DECJSONITEM(pcDecodeData, json, str)do{ \
									cJSON *item = cJSON_GetObjectItem(json, str); \
									if(str[0] == 'i') \
										pcDecodeData->##str## = item->valueint; \
									else if(str[0] == 'f' || str[0] == 'd') \
										pcDecodeData->##str## = item->valuedouble; \
									else \
										pcDecodeData->##str## = item->valuestring; \
								}while(0); 
#define TEST(STR) 111##STR###
int testDecodeJson(const char *pcDecodeData)
{
	cJSON           *json;
	json=cJSON_Parse("{\"firstName\":\"Brett\"}");
	//printf("%s", cJSON_Print(json));
	cJSON *item = cJSON_GetObjectItem(json,"firstName");  //
	printf("firstName:%s\n",item->valuestring);
	return 0;
}

void pyDec_getJsonStr(AnalysParam *pstDecodeData, const char *pcDecodeData)
{
	cJSON *pJsonData = NULL;
	ZUINT i = 0;
	pJsonData = cJSON_Parse(pcDecodeData);
	printf("%ld \n", sizeof(cJsonLst) / sizeof(char *));
	for(; i < sizeof(cJsonLst) / sizeof(char *); i++)
	{
		//printf("%s \n", TEST("222"));
		//DECJSONITEM(pcDecodeData, pJsonData, cJsonLst[i]);
	}
	//TEST("111");
}

int main(int argc, const char *argv[])
{
	AnalysParam stDecodeData;
	pyDec_getJsonStr(&stDecodeData, argv[1]);

	//get stDecodeData do decode data
}
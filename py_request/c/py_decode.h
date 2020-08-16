#ifndef PY_DECODE_h
#define PY_DECODE_h

#include <stdbool.h>

typedef int             ZINT;
typedef unsigned int    ZUINT; 
typedef short           ZSHORT;
typedef unsigned short  ZUCHORT;
typedef char            ZCHAR;
typedef unsigned char   ZUCHAR;
typedef float           ZFLOAT;
typedef double          ZDOUBLE;
typedef bool            ZBOOL;

typedef struct
{
    // 亚赔变化表 （只需澳门）
}HCLST;
 

typedef struct
{
    ZINT iHomeRank;   // 主队排名
    ZINT iHomeRecentWin; // 主队近期战绩胜场次
    ZINT iHomeRecentDraws; // 主队近期战绩平场次
    ZINT iHomeRecentLose; // 主队近期战绩负场次

    ZINT iAwayRank;    // 客队排名
    ZINT iAwayRecentWin; // 客队近期战绩胜场次
    ZINT iAwayRecentDraws; // 客队近期战绩平场次
    ZINT iAwayRecentLose; // 客队近期战绩负场次

    ZINT iVsRecHomeWin; // 对赛往绩主队胜场次
    ZINT iVsRecHomeDraws; // 对赛往绩主队平场次
    ZINT iVsRecHomeLose; // 对赛往绩主队负场次

    ZINT iQdsa ; // qdsa让球数据

    ZFLOAT  fInitialHandicapX; // 即时指数让球初盘（澳门）
    ZFLOAT  fInitialHandicapOver; // 即时指数让球初盘上盘赔率（澳门）
    ZFLOAT  fInitialHandicapUnder; // 即时指数让球初盘下盘赔率（澳门）
    ZFLOAT  fInstantHandicapX; // 即时指数让球实时盘（澳门） 最后一次赔率变化
    ZFLOAT  fInstantHandicapOver; // 即时指数让球实时盘上盘赔率（澳门）
    ZFLOAT  fInstantHandicapUnder; // 即时指数让球实时盘下盘赔率（澳门）
    HCLST   *pstHandicapList;  // 亚赔变化表 （只需澳门）

    ZFLOAT  fInitialHandicapX_crown; // 即时指数让球初盘（皇冠）
    ZFLOAT  fInitialHandicapOver_crown; // 即时指数让球初盘上盘赔率（皇冠）
    ZFLOAT  fInitialHandicapUnder_crown; // 即时指数让球初盘下盘赔率（皇冠）
    ZFLOAT  fInstantHandicapX_crown; // 即时指数让球实时盘（皇冠） 最后一次赔率变化
    ZFLOAT  fInstantHandicapOver_crown; // 即时指数让球实时盘上盘赔率（皇冠）
    ZFLOAT  fInstantHandicapUnder_crown; // 即时指数让球实时盘下盘赔率（皇冠）  
    
}AnalysParam;

const char *cJsonLst[] = 
{
    "iHomeRank",
    "iHomeRecentWin",
    "iHomeRecentDraws",
    "iHomeRecentLose",

    "iAwayRank",
    "iAwayRecentWin",
    "iAwayRecentDraws",
    "iAwayRecentLose",

    "iVsRecHomeWin",
    "iVsRecHomeDraws",
    "iVsRecHomeLose",

    "iQdsa",

    "fInitialHandicapX",
    "fInitialHandicapOver",
    "fInitialHandicapUnder",
    "fInstantHandicapX",
    "fInstantHandicapOver",
    "fInstantHandicapUnder",
    "pstHandicapList",

    "fInitialHandicapX_crown",
    "fInitialHandicapOver_crown",
    "fInitialHandicapUnder_crown",
    "fInstantHandicapX_crown",
    "fInstantHandicapOver_crown",
    "fInstantHandicapUnder_crown",
};

#endif
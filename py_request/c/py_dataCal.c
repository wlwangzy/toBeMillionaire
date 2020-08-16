#include <stdio.h>
#include "py_decode.h"

typedef enum
{
	HOME_TEAM,
	AWAY_TEAM
}TEAM;

typedef enum
{
	LOWER,
	UPPER
}HANDI_QDSA;

ZFLOAT qdsaToHandicap(ZINT qdsa)
{
	ZFLOAT handicap = 0.0;

	if (qdsa >= 0 && qdsa < 25)
		qdsaToHandicap = 0.25;
	else if (qdsa >= 25 && qdsa < 50)
		qdsaToHandicap =  0.5;
	else if (qdsa >= 50 && qdsa < 75)
		qdsaToHandicap =  0.75;
	else if (qdsa >= 75 && qdsa < 100)
		qdsaToHandicap =  1.0;
	else if (qdsa >= 100 && qdsa < 125)
		qdsaToHandicap = 1.25;
	else if (qdsa >= 125 && qdsa < 150)
		qdsaToHandicap = 1.5;
	else if (qdsa >= 150 && qdsa < 175)
	 	qdsaToHandicap = 1.75;
	else if (qdsa >= 175 && qdsa < 200)
	 	qdsaToHandicap = 2.0;
	else if (qdsa >= 200 && qdsa < 225)
	 	qdsaToHandicap = 2.25;
	else if (qdsa >= 225 && qdsa < 250)
	 	qdsaToHandicap = 2.5;
	else if (qdsa >= 275 && qdsa < 300)
	  	qdsaToHandicap = 2.75;		  
	else if (qdsa >= -25 && qdsa < 0)
		qdsaToHandicap = 0.0;
	else if (qdsa >= -50 && qdsa < -25)
	 	qdsaToHandicap = -0.25;
	else if (qdsa >= -75 && qdsa < -50)
	  	qdsaToHandicap = -0.5;
	else if (qdsa >= -100 && qdsa < -75)
	  	qdsaToHandicap = -0.75;
	else if (qdsa >= -125 && qdsa < -100)
		qdsaToHandicap = -1.0;
	else if (qdsa >= -150 && qdsa < -125)
	   	qdsaToHandicap = -1.25;
	else if (qdsa >= -175 && qdsa < -150)
	  	qdsaToHandicap = -1.5;
	else if (qdsa >= -200 && qdsa < -175)
	  	qdsaToHandicap = -1.75;
	else if (qdsa >= -225 && qdsa < -200)
	  	qdsaToHandicap = -2.0;
	else if (qdsa >= -250 && qdsa < -225)
	  	qdsaToHandicap = -2.25;
	else if (qdsa >= -300 && qdsa < -275)
	  	qdsaToHandicap = -2.5;
	else
	{
		printf("unknow qdsa %d\n",qdsa);
		handicap = 0.0;
	}
		  
	return handicap;
}

// 返回值 0:主队赢盘，1:客队赢盘  -1:无法判断
int pyDataCal(AnalysParam *pstDecodeData)
{
	int homeScore = 0,awayScore = 0;
	ZFLOAT qdsaHandicap = 0.0; // qdsa换算盘口
	bool isHandicaUpperpQdsa;// 开出的盘口是否高于qdsa换算盘口 1:是 0:否
	bool stateBetterTeam;// 实力更好的球队0:主队 1:客队
	bool strengthBetterTeam; // 实力更好的球队 0:主队 1:客队

	printf("homeRank %d\n",pstDecodeData->iHomeRank);
	printf("iHomeRecentWin %d\n",pstDecodeData->iHomeRecentWin);
	printf("iHomeRecentDraws %d\n",pstDecodeData->iHomeRecentDraws);
	printf("iHomeRecentLose %d\n",pstDecodeData->iHomeRecentLose);
	printf("iAwayRank %d\n",pstDecodeData->iAwayRank);
	printf("iAwayRecentWin %d\n",pstDecodeData->iAwayRecentWin);
	printf("iAwayRecentDraws %d\n",pstDecodeData->iAwayRecentDraws);
	printf("iAwayRecentLose %d\n",pstDecodeData->iAwayRecentLose);
	printf("iVsRecHomeWin %d\n",pstDecodeData->iVsRecHomeWin);
	printf("iVsRecHomeDraws %d\n",pstDecodeData->iVsRecHomeDraws);
	printf("iVsRecHomeLose %d\n",pstDecodeData->iVsRecHomeLose);
	printf("@@@@@@@@@@@@iQdsa %d\n",pstDecodeData->iQdsa);
	printf("fInitialHandicapX %f\n",pstDecodeData->fInitialHandicapX);
	printf("fInitialHandicapOver %f\n",pstDecodeData->fInitialHandicapOver);
	printf("fInitialHandicapUnder %f\n",pstDecodeData->fInitialHandicapUnder);
	printf("fInstantHandicapX %f\n",pstDecodeData->fInstantHandicapX);
	printf("fInstantHandicapOver %f\n",pstDecodeData->fInstantHandicapOver);
	printf("fInstantHandicapUnder %f\n",pstDecodeData->fInstantHandicapUnder);
	printf("fInitialHandicapX_crown %f\n",pstDecodeData->fInitialHandicapX_crown);
	printf("fInitialHandicapOver_crown %f\n",pstDecodeData->fInitialHandicapOver_crown);
	printf("fInitialHandicapUnder_crown %f\n",pstDecodeData->fInitialHandicapUnder_crown);
	printf("fInstantHandicapX_crown %f\n",pstDecodeData->fInstantHandicapX_crown);
	printf("fInstantHandicapOver_crown %f\n",pstDecodeData->fInstantHandicapOver_crown);
	printf("fInstantHandicapUnder_crown %f\n",pstDecodeData->fInstantHandicapUnder_crown);

//# 1. 广实分析【主队作为基准】
//# 1.1 排名对比，排名值小的为理论优势方。优势方得1分
	if (pstDecodeData->iHomeRank > pstDecodeData->iAwayRank)
	{
		homeScore += 1;
	}
	else if (pstDecodeData->iHomeRank < pstDecodeData->iAwayRank)
	{
		awayScore += 1;
	}
	printf("1.1 homeScore %d awayScore %d\n",homeScore,awayScore)
//# 1.2 对赛往绩对比，胜多的一方为优势方。优势方得4分
	if (pstDecodeData->iVsRecHomeWin > pstDecodeData->iVsRecHomeLose)
	{
		homeScore += 4;
	}
	else if (pstDecodeData->iVsRecHomeWin < pstDecodeData->iVsRecHomeLose)
	{
		awayScore += 4;
	}
	printf("1.2 homeScore %d awayScore %d\n",homeScore,awayScore)
//# 1.3 近期战绩对比，对比10场，胜+平多的一方为优势方。优势方得2分
	if (pstDecodeData->iHomeRecentWin + pstDecodeData->iHomeRecentDraws > 
		pstDecodeData->iAwayRecentWin + pstDecodeData->iAwayRecentDraws)
	{
		homeScore += 2;
	}
	else if (pstDecodeData->iHomeRecentWin + pstDecodeData->iHomeRecentDraws < 
		pstDecodeData->iAwayRecentWin + pstDecodeData->iAwayRecentDraws)
	{
		awayScore += 2;
	}
	printf("1.3 homeScore %d awayScore %d\n",homeScore,awayScore)
//# 1.4 在近期战绩的基础上，查看主队主场战绩，客队客场战绩。胜+平多的一方为优势方。优势方得3分
//# 1.5 综合两队优势得分，分高的为主观优势方。资金对优势方会有偏爱。若得分一致，主队为优势方
	if (homeScore >= awayScore)
	{
		stateBetterTeam = HOME_TEAM;
	}
	else
	{
		stateBetterTeam = AWAY_TEAM;
	}

//# 2. 数据转换
//# 2.1 获取澳门盘口初盘让球数据【以实力强的让球方为基准】
//# 2.2 获取qdsa让球数据
//# 2.3 是否存在qdsa
//# 2.3.1 存在，根据qdsa换算表，算出qdsa对应的让球能力
	qdsaHandicap = qdsaToHandicap(pstDecodeData->iQdsa);
//# 2.3.2 不存在，对比对赛往绩的近期及近几年平均让球能力【暂时可忽略不做】
//# 2.4 对比澳门初盘让球数据和qdsa对应的让球能力。qdsa让球作为基准，澳门盘高于它，为高开，低于它为低开
	if (fabs(pstDecodeData->fInitialHandicapX - qdsaHandicap) < 1e-6)
	{
		printf("qdsaHandicap == initialHandicap\n");
		return -1;
	}

	// 判断让球方是否高开
	if (fabs(pstDecodeData->fInitialHandicapX) > fabs(qdsaHandicap))
	{
		isHandicaUpperpQdsa	= UPPER;
	}
	else
	{
		isHandicaUpperpQdsa	= LOWER;
	}	
	// 让球方是主队还是客队
	if (pstDecodeData->fInitialHandicapX >= 0.0)
	{
s		trengthBetterTeam = HOME_TEAM;
	}
	else
	{
		trengthBetterTeam = AWAY_TEAM;
	}

//# 2.5 看是否满足以下模型：
//# 2.5.1 高开阻上模型（新手常用）：
////#       解释：让球方没有优势，受让方题材大（拉力大），菠菜高开盘口，增加门槛，阻碍彩民去上盘，
//#             逼着她们往更优势的下盘走。
//#       分析思路：从广实分析可以得到，受让方为优势方。让球方开出的澳门盘口，高于qdsa盘口。
//#                 同时配合澳门盘口的走势，临场临场维持低水或降盘到低一级盘口低水。
//#       结论：让球方赢盘
	if (trengthBetterTeam == HOME_TEAM) && (stateBetterTeam == AWAY_TEAM) 
		&& (isHandicaUpperpQdsa == UPPER)
	{
		printf("高开阻上模型,主队让球且高开，主队赢盘\n");
		return 0;
	}

	if (trengthBetterTeam == AWAY_TEAM) && (stateBetterTeam == HOME_TEAM) 
		&& (isHandicaUpperpQdsa == UPPER)
	{
		printf("高开阻上模型,客队让球且高开，客队赢盘\n");
		return 1;
	}
//# 2.5.2 浅开诱上模型（新手常用）
//#       解释：让球方优势极大 题材不小 利好很多，受让方弱势（拉力小），
//#             菠菜浅开了一种低门槛的盘口，俗称笋盘，这种盘让彩民舒舒服服的介入，通常杀伤力巨大。
//#       分析思路：从广实分析可以得到，让球方为优势方。让球方开出的澳门盘口，低于qdsa盘口。
//#                 同时配合澳门盘口的走势，临场维持高水或升盘到高一级盘口高水。
//#       结论：让球方输盘
	if (trengthBetterTeam == HOME_TEAM) && (stateBetterTeam == HOME_TEAM) && 
		(isHandicaUpperpQdsa == LOWER)
	{
		printf("浅开诱上模型,主队让球且低开，客队赢盘\n");
		return 1;
	}

	if (trengthBetterTeam == AWAY_TEAM) && (stateBetterTeam == AWAY_TEAM) 
		&& (isHandicaUpperpQdsa == LOWER)
	{
		printf("浅开诱上模型,客队让球且低开，主队赢盘\n");
		return 0;
	}
//# 2.5.3 高开诱上模型
//#       解释：让球方优势极大 题材不小 利好很多，受让方弱势（拉力小），两队差距很大。
//#             但是菠菜高开了多级盘口，一般两级以上，这种盘让彩民进一步认为优势方必赢，多半有坑。
//#       分析思路：从广实分析可以得到，让球方为优势方。让球方开出的澳门盘口，高于qdsa盘口两级及以上。
//#                 同时配合澳门盘口的走势，盘口高开，临场维持高水或者还继续升盘到高一级盘口高水。
//#       结论：让球方输盘
	if (trengthBetterTeam == HOME_TEAM) && (stateBetterTeam == HOME_TEAM) 
		&& (isHandicaUpperpQdsa == UPPER)
	{
		printf("高开诱上模型,主队让球且高开，客队赢盘\n");
		return 1;
	}

	if (trengthBetterTeam == AWAY_TEAM) && (stateBetterTeam == AWAY_TEAM) 
		&& (isHandicaUpperpQdsa == UPPER)
	{
		printf("高开诱上模型,客队让球且高开，主队赢盘\n");
		return 0;
	}
//# 2.5.4 浅开反诱上盘
//#       解释：一般用于强队对弱队，但是强队近况不好，弱队近况很好。
//#             但是菠菜低开了多级盘口，一般两级以上，这种盘让彩民认为强队要爆冷。
// #       分析思路：从广实分析可以得到，强队排名远高于弱队，但是因为弱队近况好，优势分差不多，
// #                 甚至弱队反而是优势方。让球方开出的澳门盘口，低于qdsa盘口两级及以上。
// #                 同时配合澳门盘口的走势，盘口低开，继续不断降盘到低一级甚至两球盘口低水。
// #       结论：让球方赢盘
	if (trengthBetterTeam == HOME_TEAM) && (stateBetterTeam == AWAY_TEAM) 
		&& (isHandicaUpperpQdsa == LOWER)
	{
		printf("浅开反诱模型,主队让球且低开，主队赢盘\n");
		return 0;
	}

	if (trengthBetterTeam == AWAY_TEAM) && (stateBetterTeam == HOME_TEAM) 
		&& (isHandicaUpperpQdsa == LOWER)
	{
		printf("浅开反诱模型,客队让球且低开，客队赢盘\n");
		return 1;
	}
// # 2.5.5 高开反诱上盘
// #       解释：双方广实力对比，两队实力均很强，且两队实力差异很小。
// #             但是菠菜高开了多级盘口，一般两级以上，这种盘庄家故意设置不平衡盘口，让彩民有倾向性。
// #       分析思路：从广实分析可以得到，让球方为优势方。让球方开出的澳门盘口，高于qdsa盘口两级及以上。
// #                 同时配合澳门盘口的走势，盘口高开，临场维持高水或者还继续升盘到高一级盘口高水。
// #       结论：让球方输盘

}

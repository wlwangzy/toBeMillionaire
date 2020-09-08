#include <stdio.h>
#include <math.h>
#include "py_decode.h"

typedef enum
{
	HOME_TEAM,
	AWAY_TEAM
}TEAM;

typedef enum
{
	LOWER_S,  //低开两级及以上
	LOWER,	  //低开一级
	EQUAL,    //平开
	UPPER,    //高开
	UPPER_S   //高开两级及以上
}HANDI_QDSA;

typedef enum
{
	LOW_ODDS,  		//低水 <0.82
	LOW_MID_ODDS,	//中低水 0.82-0.88
	MID_ODDS,    	//中水 0.88-0.92
	MID_HIGH_ODDS,  //中高水 0.92-0.98
	HIGH_ODDS   	//高水 >0.98
}ODDS_LEVEL;

typedef struct
{
	ZFLOAT handicap;
	ZINT oddLevel;
}QDSA_CFG;

// 以baseHandicap为基准，判断盘口较baseHandicap的高开低开等级
int AbsLEVEL(ZFLOAT compareHandicap, ZFLOAT baseHandicap)
{
	int level,absLevel;
	level = fabs(compareHandicap - baseHandicap)/0.25;

	if ((fabs(compareHandicap) > fabs(baseHandicap)) && (level == 1))
	{
		absLevel = UPPER;
	}
	else if ((fabs(compareHandicap) > fabs(baseHandicap)) && (level > 1))
	{
		absLevel = UPPER_S;
	}
	else if ((fabs(compareHandicap) < fabs(baseHandicap)) && (level == 1))
	{
		absLevel = LOWER;
	}
	else if ((fabs(compareHandicap) < fabs(baseHandicap)) && (level > 1))
	{
		absLevel = LOWER_S;
	}
	else
	{
		absLevel = EQUAL;
	}
	return absLevel;
}

QDSA_CFG qdsaToHandicap(ZINT qdsa)
{
	QDSA_CFG qdsaCfg;
	ZFLOAT oddSt = 0.0;

	if (qdsa >= 0 && qdsa < 25)
		qdsaCfg.handicap = 0.25;
	else if (qdsa >= 25 && qdsa < 50)
		qdsaCfg.handicap =  0.5;
	else if (qdsa >= 50 && qdsa < 75)
		qdsaCfg.handicap =  0.75;
	else if (qdsa >= 75 && qdsa < 100)
		qdsaCfg.handicap =  1.0;
	else if (qdsa >= 100 && qdsa < 125)
		qdsaCfg.handicap = 1.25;
	else if (qdsa >= 125 && qdsa < 150)
		qdsaCfg.handicap = 1.5;
	else if (qdsa >= 150 && qdsa < 175)
	 	qdsaCfg.handicap = 1.75;
	else if (qdsa >= 175 && qdsa < 200)
	 	qdsaCfg.handicap = 2.0;
	else if (qdsa >= 200 && qdsa < 225)
	 	qdsaCfg.handicap = 2.25;
	else if (qdsa >= 225 && qdsa < 250)
	 	qdsaCfg.handicap = 2.5;
	else if (qdsa >= 275 && qdsa < 300)
	  	qdsaCfg.handicap = 2.75;		  
	else if (qdsa >= -25 && qdsa < 0)
		qdsaCfg.handicap = 0.0;
	else if (qdsa >= -50 && qdsa < -25)
	 	qdsaCfg.handicap = -0.25;
	else if (qdsa >= -75 && qdsa < -50)
	  	qdsaCfg.handicap = -0.5;
	else if (qdsa >= -100 && qdsa < -75)
	  	qdsaCfg.handicap = -0.75;
	else if (qdsa >= -125 && qdsa < -100)
		qdsaCfg.handicap = -1.0;
	else if (qdsa >= -150 && qdsa < -125)
	   	qdsaCfg.handicap = -1.25;
	else if (qdsa >= -175 && qdsa < -150)
	  	qdsaCfg.handicap = -1.5;
	else if (qdsa >= -200 && qdsa < -175)
	  	qdsaCfg.handicap = -1.75;
	else if (qdsa >= -225 && qdsa < -200)
	  	qdsaCfg.handicap = -2.0;
	else if (qdsa >= -250 && qdsa < -225)
	  	qdsaCfg.handicap = -2.25;
	else if (qdsa >= -300 && qdsa < -275)
	  	qdsaCfg.handicap = -2.5;
	else
	{
		printf("unknow qdsa %d\n",qdsa);
		qdsaCfg.handicap = 0.0;
	}
	oddSt = qdsa / (qdsaCfg.handicap * 5);
	if (oddSt < 0.4)
		qdsaCfg.oddLevel = LOW_ODDS;
	else if (oddSt < 0.8)
		qdsaCfg.oddLevel = LOW_MID_ODDS;
	else if (oddSt < 1.2)
		qdsaCfg.oddLevel = MID_ODDS;
	else if (oddSt < 1.6)
		qdsaCfg.oddLevel = MID_HIGH_ODDS;
	else
		qdsaCfg.oddLevel = HIGH_ODDS;
	
	return qdsaCfg;
}

// 返回值 0:主队赢盘，1:客队赢盘  -1:无法判断
int pyDataCal(AnalysParam *pstDecodeData)
{
	int homeScore = 0,awayScore = 0;
	QDSA_CFG qdsaHandicap; // qdsa换算盘口
	int isHandicaUpperpQdsa;// 开出的盘口是否高于qdsa换算盘口 1:是 0:否
	bool stateBetterTeam;// 实力更好的球队0:主队 1:客队
	bool strengthBetterTeam; // 实力更好的球队 0:主队 1:客队
	int iRank,iRankAbs;

	printf("***************************************\n");
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
	printf("fInitialHandicapX %0.2f\n",pstDecodeData->fInitialHandicapX);
	printf("fInitialHandicapOver %0.2f\n",pstDecodeData->fInitialHandicapOver);
	printf("fInitialHandicapUnder %0.2f\n",pstDecodeData->fInitialHandicapUnder);
	printf("fInstantHandicapX %0.2f\n",pstDecodeData->fInstantHandicapX);
	printf("fInstantHandicapOver %0.2f\n",pstDecodeData->fInstantHandicapOver);
	printf("fInstantHandicapUnder %0.2f\n",pstDecodeData->fInstantHandicapUnder);
	printf("fInitialHandicapX_crown %0.2f\n",pstDecodeData->fInitialHandicapX_crown);
	printf("fInitialHandicapOver_crown %0.2f\n",pstDecodeData->fInitialHandicapOver_crown);
	printf("fInitialHandicapUnder_crown %0.2f\n",pstDecodeData->fInitialHandicapUnder_crown);
	printf("fInstantHandicapX_crown %0.2f\n",pstDecodeData->fInstantHandicapX_crown);
	printf("fInstantHandicapOver_crown %0.2f\n",pstDecodeData->fInstantHandicapOver_crown);
	printf("fInstantHandicapUnder_crown %0.2f\n",pstDecodeData->fInstantHandicapUnder_crown);
	printf("***************************************\n\n");

//# 1. 广实分析【主队作为基准】
	homeScore = pstDecodeData->iHomeRecentWin * 3 + pstDecodeData->iHomeRecentDraws;
	awayScore = pstDecodeData->iAwayRecentWin * 3 + pstDecodeData->iAwayRecentDraws;
	printf("1.0 homeScore %d awayScore %d\n",homeScore,awayScore);
//# 1.1 排名对比，排名值小的为理论优势方。根据联赛球队个数，越靠前得分越高
	iRank = pstDecodeData->iHomeRank - pstDecodeData->iAwayRank;
	iRankAbs = abs(iRank)/3; // 三名内认为是同一档
	if (iRank < 0) // 主队排名高，给主队加分
	{
		homeScore += iRankAbs;
	}
	else
	{
		awayScore += iRankAbs;
	}	
	printf("1.1 homeScore %d awayScore %d\n",homeScore,awayScore);
//# 1.2 对赛往绩对比，胜多的一方为优势方。
	homeScore += pstDecodeData->iVsRecHomeWin * 3;
	awayScore += pstDecodeData->iVsRecHomeLose * 3;
	printf("1.2 homeScore %d awayScore %d\n",homeScore,awayScore);
//# 1.3 近期战绩对比，对比10场，胜+平多的一方为优势方。放在广实当基础分
	//homeScore += pstDecodeData->iHomeRecentWin * 3 + pstDecodeData->iHomeRecentDraws;
	//awayScore += pstDecodeData->iAwayRecentWin * 3 + pstDecodeData->iAwayRecentDraws;
	//printf("1.3 homeScore %d awayScore %d\n",homeScore,awayScore)
//# 1.4 在近期战绩的基础上，查看主队主场战绩，客队客场战绩。胜+平多的一方为优势方。
	//homeScore += pstDecodeData->iHomeRecentHomeWin * 3 + pstDecodeData->iHomeRecentHomeDraws;
	//awayScore += pstDecodeData->iAwayRecentAwayWin * 3 + pstDecodeData->iAwayRecentAwayDraws;
	//printf("1.4 homeScore %d awayScore %d\n",homeScore,awayScore)
//# 1.5 综合两队优势得分，分高的为主观优势方。资金对优势方会有偏爱。若得分一致，主队为优势方
	if (homeScore >= awayScore)
	{
		stateBetterTeam = HOME_TEAM;
	}
	else
	{
		stateBetterTeam = AWAY_TEAM;
	}
	printf("stateBetterTeam is %d\n",stateBetterTeam);

//# 2. 数据转换
//# 2.1 获取澳门盘口初盘让球数据【以实力强的让球方为基准】
//# 2.2 获取qdsa让球数据
//# 2.3 是否存在qdsa
//# 2.3.1 存在，根据qdsa换算表，算出qdsa对应的让球能力
	qdsaHandicap = qdsaToHandicap(pstDecodeData->iQdsa);
	printf("qdsaHandicap.handicap is %0.2f oddLevel is %d\n",qdsaHandicap.handicap,qdsaHandicap.oddLevel);

//# 2.3.2 不存在，对比对赛往绩的近期及近几年平均让球能力【暂时可忽略不做】
//# 2.4 对比澳门初盘让球数据和qdsa对应的让球能力。qdsa让球作为基准，澳门盘高于它，为高开，低于它为低开


	// 判断让球方是否高开,几高开等级
	isHandicaUpperpQdsa = AbsLEVEL(pstDecodeData->fInitialHandicapX, qdsaHandicap.handicap);
	printf("isHandicaUpperpQdsa is %d\n",isHandicaUpperpQdsa);

	// 让球方是主队还是客队
	if (pstDecodeData->fInitialHandicapX < 0.0)
	{
		strengthBetterTeam = AWAY_TEAM;
	}
	else
	{
		strengthBetterTeam = HOME_TEAM;
	}
	printf("strengthBetterTeam %d\n",strengthBetterTeam);

	if (fabs(pstDecodeData->fInitialHandicapX - qdsaHandicap.handicap) < 1e-6)
	{
		if (fabs(qdsaHandicap.handicap) < 1e-6)
		{
			printf("平手盘，盘口相同\n");	
			if ((strengthBetterTeam == HOME_TEAM) && (stateBetterTeam == AWAY_TEAM))
			{
				if (AbsLEVEL(pstDecodeData->fInitialHandicapX, pstDecodeData->fInstantHandicapX) == EQUAL
					&& (pstDecodeData->fInitialHandicapOver < 0.88) 
					&& (pstDecodeData->fInstantHandicapOver < 0.88)
					&& (pstDecodeData->fInitialHandicapOver < pstDecodeData->fInstantHandicapOver))
				{
					printf("二次确认,初盘终盘不变上盘保持低水水位有上升 主队赢盘 80% \n");
				}
				return 0;
			}
			return -1;
		}
		else
		{
			printf("非平手盘，盘口相同，放弃\n");
			return -1;
		}
	}
//# 2.5 看是否满足以下模型：
//# 2.5.1 高开阻上模型（新手常用）：
////#       解释：让球方没有优势，受让方题材大（拉力大），菠菜高开盘口，增加门槛，阻碍彩民去上盘，
//#             逼着她们往更优势的下盘走。
//#       分析思路：从广实分析可以得到，受让方为优势方。让球方开出的澳门盘口，高于qdsa盘口。
//#                 同时配合澳门盘口的走势，临场临场维持低水或降盘到低一级盘口低水。
//#       结论：让球方赢盘
	if ((strengthBetterTeam == HOME_TEAM) && (stateBetterTeam == AWAY_TEAM) 
		&& (isHandicaUpperpQdsa == UPPER))
	{
		printf("高开阻上模型,主队让球且高开\n");

		if (AbsLEVEL(pstDecodeData->fInitialHandicapX, pstDecodeData->fInstantHandicapX) == EQUAL
			&& (pstDecodeData->fInitialHandicapOver < 0.88) 
			&& (pstDecodeData->fInstantHandicapOver < 0.88))
		{
			printf("二次确认,初盘终盘不变且均保持低水 主队赢盘 80%\n");
		}
		else if (AbsLEVEL(pstDecodeData->fInstantHandicapX, pstDecodeData->fInitialHandicapX) == LOWER
			&& (pstDecodeData->fInitialHandicapOver > 0.95) 
			&& (pstDecodeData->fInstantHandicapOver < 0.88))
		{
			printf("二次确认,初盘高水终盘降盘保持低水 主队赢盘 90%\n");
		}
		else
		{
			printf("初盘判断：主队赢盘 60% \n");
		}
		
		return 0;
	}

	if ((strengthBetterTeam == AWAY_TEAM) && (stateBetterTeam == HOME_TEAM) 
		&& (isHandicaUpperpQdsa == UPPER))
	{
		printf("高开阻上模型,客队让球且高开\n");
		
		if (AbsLEVEL(pstDecodeData->fInitialHandicapX, pstDecodeData->fInstantHandicapX) == EQUAL
			&& (pstDecodeData->fInitialHandicapOver < 0.88) 
			&& (pstDecodeData->fInstantHandicapOver < 0.88))
		{
			printf("二次确认,初盘终盘不变且均保持低水 客队赢盘 80%\n");
		}
		else if (AbsLEVEL(pstDecodeData->fInstantHandicapX, pstDecodeData->fInitialHandicapX) == LOWER
			&& (pstDecodeData->fInitialHandicapOver > 0.95) 
			&& (pstDecodeData->fInstantHandicapOver < 0.88))
		{
			printf("二次确认,初盘高水终盘降盘保持低水 客队赢盘 90%\n");
		}
		else
		{
			printf("初盘判断：客队赢盘 60% \n");
		}
		return 1;
	}
//# 2.5.2 浅开诱上模型（新手常用）
//#       解释：让球方优势极大 题材不小 利好很多，受让方弱势（拉力小），
//#             菠菜浅开了一种低门槛的盘口，俗称笋盘，这种盘让彩民舒舒服服的介入，通常杀伤力巨大。
//#       分析思路：从广实分析可以得到，让球方为优势方。让球方开出的澳门盘口，低于qdsa盘口。
//#                 同时配合澳门盘口的走势，临场维持高水或升盘到高一级盘口高水。
//#       结论：让球方输盘
	if ((strengthBetterTeam == HOME_TEAM) && (stateBetterTeam == HOME_TEAM) && 
		(isHandicaUpperpQdsa == LOWER))
	{
		printf("浅开诱上模型,主队让球且低开\n");
		
		if (AbsLEVEL(pstDecodeData->fInitialHandicapX, pstDecodeData->fInstantHandicapX) == EQUAL
			&& (pstDecodeData->fInitialHandicapOver > 0.95) 
			&& (pstDecodeData->fInstantHandicapOver > 0.95))
		{
			printf("二次确认,初盘终盘不变且均保持高水 客队赢盘 80%\n");
		}
		else if (AbsLEVEL(pstDecodeData->fInstantHandicapX, pstDecodeData->fInitialHandicapX) == UPPER
			&& (pstDecodeData->fInitialHandicapOver < 0.88) 
			&& (pstDecodeData->fInstantHandicapOver > 0.95))
		{
			printf("二次确认,初盘低水终盘升盘保持高水 客队赢盘 90%\n");
		}
		else
		{
			printf("初盘判断：客队赢盘 60% \n");
		}
		return 1;
	}

	if ((strengthBetterTeam == AWAY_TEAM) && (stateBetterTeam == AWAY_TEAM) 
		&& (isHandicaUpperpQdsa == LOWER))
	{
		printf("浅开诱上模型,客队让球且低开，主队赢盘\n");
		
		if (AbsLEVEL(pstDecodeData->fInitialHandicapX, pstDecodeData->fInstantHandicapX) == EQUAL
			&& (pstDecodeData->fInitialHandicapOver > 0.95) 
			&& (pstDecodeData->fInstantHandicapOver > 0.95))
		{
			printf("二次确认,初盘终盘不变且均保持高水 主队赢盘 80%\n");
		}
		else if (AbsLEVEL(pstDecodeData->fInstantHandicapX, pstDecodeData->fInitialHandicapX) == UPPER
			&& (pstDecodeData->fInitialHandicapOver < 0.88) 
			&& (pstDecodeData->fInstantHandicapOver > 0.95))
		{
			printf("二次确认,初盘低水终盘升盘保持高水 主队赢盘 90%\n");
		}
		else
		{
			printf("初盘判断：主队赢盘 60% \n");
		}
		return 0;
	}
//# 2.5.3 高开诱上模型
//#       解释：让球方优势极大 题材不小 利好很多，受让方弱势（拉力小），两队差距很大。
//#             但是菠菜高开了多级盘口，一般两级以上，这种盘让彩民进一步认为优势方必赢，多半有坑。
//#       分析思路：从广实分析可以得到，让球方为优势方。让球方开出的澳门盘口，高于qdsa盘口两级及以上。
//#                 同时配合澳门盘口的走势，盘口高开，临场维持高水或者还继续升盘到高一级盘口高水。
//#       结论：让球方输盘
// # 2.5.5 高开反诱上盘
// #       解释：双方广实力对比，两队实力均很强，且两队实力差异很小。
// #             但是菠菜高开了多级盘口，一般两级以上，这种盘庄家故意设置不平衡盘口，让彩民有倾向性。
// #       分析思路：从广实分析可以得到，让球方为优势方。让球方开出的澳门盘口，高于qdsa盘口两级及以上。
// #                 同时配合澳门盘口的走势，盘口高开，临场维持高水或者还继续升盘到高一级盘口高水。
// #       结论：让球方输盘
	
	if (((strengthBetterTeam == HOME_TEAM) && (stateBetterTeam == HOME_TEAM))
		&& (isHandicaUpperpQdsa == UPPER_S))
	{
		if ((pstDecodeData->iHomeRecentHomeWin + pstDecodeData->iHomeRecentHomeDraws > 8)
			&& (pstDecodeData->iAwayRecentAwayWin + pstDecodeData->iAwayRecentAwayDraws > 8))
		{			
			printf("高开反诱上盘,主队让球且高开\n");
		}
		else
		{
			printf("高开诱上模型,主队让球且高开\n");
		}	
				
		if (AbsLEVEL(pstDecodeData->fInitialHandicapX, pstDecodeData->fInstantHandicapX) == EQUAL
			&& (pstDecodeData->fInitialHandicapOver > 0.95) 
			&& (pstDecodeData->fInstantHandicapOver > 0.87))
		{
			if (pstDecodeData->fInitialHandicapOver > pstDecodeData->fInstantHandicapOver)
			{
				printf("二次确认,初盘终盘不变,上盘有走热迹象且均保持较高水 客队赢盘 80%\n");
			}
			else
			{
				printf("二次确认,初盘终盘不变,上盘无走热迹象，不符合高开诱上模型，需人工确认\n");
				return -1;
			}
			
		}
		else if (AbsLEVEL(pstDecodeData->fInstantHandicapX, pstDecodeData->fInitialHandicapX) == UPPER
			&& (pstDecodeData->fInstantHandicapOver > 0.95))
		{
			printf("二次确认,无视初盘水位，终盘升盘保持高水 客队赢盘 90%\n");
		}
		else
		{
			printf("初盘判断，客队赢盘 60% \n");
		}
		return 1;
	}

	if ((strengthBetterTeam == AWAY_TEAM) && (stateBetterTeam == AWAY_TEAM) 
		&& (isHandicaUpperpQdsa == UPPER_S))
	{
		if ((pstDecodeData->iHomeRecentHomeWin + pstDecodeData->iHomeRecentHomeDraws > 8)
			&& (pstDecodeData->iAwayRecentAwayWin + pstDecodeData->iAwayRecentAwayDraws > 8))
		{			
			printf("高开反诱上盘,客队让球且高开\n");
		}
		else
		{
			printf("高开诱上模型,客队让球且高开\n");
		}	

		if (AbsLEVEL(pstDecodeData->fInitialHandicapX, pstDecodeData->fInstantHandicapX) == EQUAL
			&& (pstDecodeData->fInitialHandicapOver > 0.95) 
			&& (pstDecodeData->fInstantHandicapOver > 0.87))
		{
			if (pstDecodeData->fInitialHandicapOver > pstDecodeData->fInstantHandicapOver)
			{
				printf("二次确认,初盘终盘不变，上盘有走热迹象且均保持较高水 主队赢盘 80%\n");
			}
			else
			{
				printf("二次确认,初盘终盘不变,上盘无走热迹象，不符合高开诱上模型，需人工确认\n");
				return -1;
			}
		}
		else if (AbsLEVEL(pstDecodeData->fInstantHandicapX, pstDecodeData->fInitialHandicapX) == UPPER
			&& (pstDecodeData->fInstantHandicapOver > 0.95))
		{
			printf("二次确认,无视初盘水位，终盘升盘保持高水 主队赢盘 90%\n");
		}
		else
		{
			printf("初盘判断，主队赢盘 60% \n");
		}
		return 0;
	}
//# 2.5.4 浅开反诱上盘
//#       解释：一般用于强队对弱队，但是强队近况不好，弱队近况很好。
//#             但是菠菜低开了多级盘口，一般两级以上，这种盘让彩民认为强队要爆冷。
// #       分析思路：从广实分析可以得到，强队排名远高于弱队，但是因为弱队近况好，优势分差不多，
// #                 甚至弱队反而是优势方。让球方开出的澳门盘口，低于qdsa盘口两级及以上。
// #                 同时配合澳门盘口的走势，盘口低开，继续不断降盘到低一级甚至两球盘口低水。
// #       结论：让球方赢盘
	if ((strengthBetterTeam == HOME_TEAM) && (stateBetterTeam == AWAY_TEAM) 
		&& (isHandicaUpperpQdsa == LOWER_S))
	{
		printf("浅开反诱模型,主队让球且低开\n");

		if ((AbsLEVEL(pstDecodeData->fInstantHandicapX, pstDecodeData->fInitialHandicapX) == LOWER
			|| AbsLEVEL(pstDecodeData->fInstantHandicapX, pstDecodeData->fInitialHandicapX) == LOWER_S)
			&& (pstDecodeData->fInstantHandicapOver < 0.86))
		{
			printf("二次确认,无视初盘水位，终盘降盘一以上且保持低水 主队赢盘 90%\n");
		}
		else
		{
			printf("初盘判断，主队赢盘 60% \n");
		}
		return 0;
	}

	if ((strengthBetterTeam == AWAY_TEAM) && (stateBetterTeam == HOME_TEAM) 
		&& (isHandicaUpperpQdsa == LOWER_S))
	{
		printf("浅开反诱模型,客队让球且低开，客队赢盘\n");

		if ((AbsLEVEL(pstDecodeData->fInstantHandicapX, pstDecodeData->fInitialHandicapX) == LOWER
			|| AbsLEVEL(pstDecodeData->fInstantHandicapX, pstDecodeData->fInitialHandicapX) == LOWER_S)
			&& (pstDecodeData->fInstantHandicapOver < 0.86))
		{
			printf("二次确认,无视初盘水位，终盘降盘一以上且保持低水 客队赢盘 90%\n");
		}
		else
		{
			printf("初盘判断，客队赢盘 60% \n");
		}
		return 1;
	}
	
	return -1;
}


AnalysParam gTestGame1 = 
{
    .iHomeRank = 9,
    .iHomeRecentWin = 5, // 主队近期战绩胜场次
    .iHomeRecentDraws = 4, // 主队近期战绩平场次
    .iHomeRecentLose = 1, // 主队近期战绩负场次
    .iHomeRecentHomeWin = 6, // 主队近期战绩主场胜场次
    .iHomeRecentHomeDraws = 4, // 主队近期战绩主场平场次
    .iHomeRecentHomeLose = 0, // 主队近期战绩主场负场次

    .iAwayRank = 21,    // 客队排名
    .iAwayRecentWin = 2, // 客队近期战绩胜场次
    .iAwayRecentDraws = 3, // 客队近期战绩平场次
    .iAwayRecentLose = 5, // 客队近期战绩负场次
    .iAwayRecentAwayWin = 2, // 客队近期战绩客场胜场次
    .iAwayRecentAwayDraws = 2, // 客队近期战绩客场平场次
    .iAwayRecentAwayLose = 6, // 客队近期战绩客场负场次

    .iVsRecHomeWin = 2, // 对赛往绩主队胜场次
    .iVsRecHomeDraws = 3, // 对赛往绩主队平场次
    .iVsRecHomeLose = 2, // 对赛往绩主队负场次

    .iQdsa = 65, // qdsa让球数据

    .fInitialHandicapX = 1.5, // 即时指数让球初盘（澳门）
    .fInitialHandicapOver = 0.96, // 即时指数让球初盘上盘赔率（澳门）
    .fInitialHandicapUnder = 0.94, // 即时指数让球初盘下盘赔率（澳门）
    .fInstantHandicapX = 1.5, // 即时指数让球实时盘（澳门） 最后一次赔率变化
    .fInstantHandicapOver = 0.88, // 即时指数让球实时盘上盘赔率（澳门）
    .fInstantHandicapUnder = 0.92, // 即时指数让球实时盘下盘赔率（澳门）
    //PSTHCLST *pstHandicapList;  // 亚赔变化表 （只需澳门）
    
};


AnalysParam gTestGame2 = 
{
    .iHomeRank = 2,
    .iHomeRecentWin = 6, // 主队近期战绩胜场次
    .iHomeRecentDraws = 0, // 主队近期战绩平场次
    .iHomeRecentLose = 4, // 主队近期战绩负场次
    .iHomeRecentHomeWin = 9, // 主队近期战绩主场胜场次
    .iHomeRecentHomeDraws = 0, // 主队近期战绩主场平场次
    .iHomeRecentHomeLose = 1, // 主队近期战绩主场负场次

    .iAwayRank = 3,    // 客队排名
    .iAwayRecentWin = 7, // 客队近期战绩胜场次
    .iAwayRecentDraws = 1, // 客队近期战绩平场次
    .iAwayRecentLose = 2, // 客队近期战绩负场次
    .iAwayRecentAwayWin = 4, // 客队近期战绩客场胜场次
    .iAwayRecentAwayDraws = 1, // 客队近期战绩客场平场次
    .iAwayRecentAwayLose = 5, // 客队近期战绩客场负场次

    .iVsRecHomeWin = 3, // 对赛往绩主队胜场次
    .iVsRecHomeDraws = 4, // 对赛往绩主队平场次
    .iVsRecHomeLose = 3, // 对赛往绩主队负场次

    .iQdsa = 123, // qdsa让球数据

    .fInitialHandicapX = 0.75, // 即时指数让球初盘（澳门）
    .fInitialHandicapOver = 0.89, // 即时指数让球初盘上盘赔率（澳门）
    .fInitialHandicapUnder = 0.91, // 即时指数让球初盘下盘赔率（澳门）
    .fInstantHandicapX = 0.75, // 即时指数让球实时盘（澳门） 最后一次赔率变化
    .fInstantHandicapOver = 0.98, // 即时指数让球实时盘上盘赔率（澳门）
    .fInstantHandicapUnder = 1.02, // 即时指数让球实时盘下盘赔率（澳门）
    //PSTHCLST *pstHandicapList;  // 亚赔变化表 （只需澳门）
    
};

AnalysParam gTestGame3 = 
{
    .iHomeRank = 3,
    .iHomeRecentWin = 4, // 主队近期战绩胜场次
    .iHomeRecentDraws = 3, // 主队近期战绩平场次
    .iHomeRecentLose = 3, // 主队近期战绩负场次
    .iHomeRecentHomeWin = 7, // 主队近期战绩主场胜场次
    .iHomeRecentHomeDraws = 1, // 主队近期战绩主场平场次
    .iHomeRecentHomeLose = 2, // 主队近期战绩主场负场次

    .iAwayRank = 11,    // 客队排名
    .iAwayRecentWin = 2, // 客队近期战绩胜场次
    .iAwayRecentDraws = 3, // 客队近期战绩平场次
    .iAwayRecentLose = 5, // 客队近期战绩负场次
    .iAwayRecentAwayWin = 2, // 客队近期战绩客场胜场次
    .iAwayRecentAwayDraws = 4, // 客队近期战绩客场平场次
    .iAwayRecentAwayLose = 4, // 客队近期战绩客场负场次

    .iVsRecHomeWin = 2, // 对赛往绩主队胜场次
    .iVsRecHomeDraws = 3, // 对赛往绩主队平场次
    .iVsRecHomeLose = 5, // 对赛往绩主队负场次

    .iQdsa = -3, // qdsa让球数据

    .fInitialHandicapX = 0.0, // 即时指数让球初盘（澳门）
    .fInitialHandicapOver = 0.76, // 即时指数让球初盘上盘赔率（澳门）
    .fInitialHandicapUnder = 1.04, // 即时指数让球初盘下盘赔率（澳门）
    .fInstantHandicapX = 0.0, // 即时指数让球实时盘（澳门） 最后一次赔率变化
    .fInstantHandicapOver = 0.88, // 即时指数让球实时盘上盘赔率（澳门）
    .fInstantHandicapUnder = 0.92, // 即时指数让球实时盘下盘赔率（澳门）
    //PSTHCLST *pstHandicapList;  // 亚赔变化表 （只需澳门）
    
};

int main(int argc,char **argv)
{
	printf("test main\n");
	pyDataCal(&gTestGame1);
	pyDataCal(&gTestGame2);
	pyDataCal(&gTestGame3);

}
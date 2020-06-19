# 思路:
# 1.广实分析
# 1.1 排名对比，排名值小的为理论优势方
# 1.2 对赛往绩对比，胜多的一方为优势方
# 1.3 近期战绩对比，对比10场，胜+平多的一方为优势方
# 1.4 在近期战绩的基础上，查看主队主场战绩，客队客场战绩

# 2. 数据转换
# 2.1 获取澳门盘口初盘让球数据
# 2.2 获取qdsa让球数据
# 2.3 是否存在qdsa
# 2.3.1 存在，根据qdsa换算表，算出qdsa对应的让球能力
# 2.3.2 不存在，对比对赛往绩的近期及近几年平均让球能力【暂时可忽略不做】
# 2.4 对比澳门初盘让球数据和qdsa对应的让球能力。qdsa让球作为基准，澳门盘高于它，为高开，低于它为低开
# 2.5 看是否满足以下模型：
# 2.5.1 高开阻上模型（新手常用）
# 2.5.2 浅开诱上模型（新手常用）
# 2.5.3 高开诱上模型
# 2.5.4 浅开反诱上盘
# 2.5.5 高开反诱上盘
# 2.6 得出结论
from selenium import webdriver

# Description:
# 1.安装selenium
#    pip install selenium
# 2.下载WebDriver，并放到python.exe同级目录
#    http://npm.taobao.org/mirrors/chromedriver/
#    下载与本地电脑Chrome浏览器一样的版本

# 获取ID列表
# @return : list
#
def getIdList():

    # 目标网页URL
    url = "http://live.win007.com/"
    
    # 目标Tag : 数据table（id = 'table_live'）中的<tr>
    trTagPath = "//table[@id='table_live']/tbody/tr"
    
    # 生成Web终端，并访问目标网页URL
    driver = webdriver.Chrome()
    driver.minimize_window()
    driver.implicitly_wait(3)
    driver.get(url)

    print("")
    print("processing ...")
    print("")

    # 解析网页标签
    trTagList = driver.find_elements_by_xpath(trTagPath)
    idList = []

    for trTag in trTagList:
        if trTag.is_displayed() and ("tr1_" == trTag.get_attribute("id")[0:4]) :
            idList.append(trTag.get_attribute("id")[4:])
    
    # 关闭Web终端
    driver.close()
    
    print("")
    print("process over!")
    print("")
    
    # 返回结果
    return idList


# ********** 启动程序，调用函数 **********
#
retList = getIdList()

print("===========")
for id in retList:
    print(id)

print("-----------")
print(len(retList))
print("===========")